import json

from app.compatibility.hermes_request import (
    CurrentDslItem,
    GlobalQueryParameters,
    HermesChatMessage,
    VmChatInput,
)
from app.context.manager import ContextManager
from app.session.manager import SessionManager
from app.session.store import SqliteSessionStore


def make_input(message: str, current_dsls=None, selected=None, history=None):
    return VmChatInput(
        userMessage=message,
        selectedBlockId=selected,
        currentDsls=current_dsls or [],
        globalQueryParameters=GlobalQueryParameters(
            names=["fundCode"],
            nonemptyFlags={"fundCode": True},
        ),
        historyMessages=history or [],
    )


def make_block(block_id: str, title: str, transform_size: int = 10):
    return CurrentDslItem(
        blockId=block_id,
        id=f"dsl-{block_id}",
        title=title,
        viewType="table",
        dsl={
            "action": "update",
            "id": f"dsl-{block_id}",
            "requests": [
                {
                    "id": f"req-{block_id}",
                    "moduleId": f"module-{block_id}",
                    "sqlCode": f"sql-{block_id}",
                }
            ],
            "transform": {
                "language": "javascript",
                "function": "function transform(responses) {" + ("x" * transform_size) + "}",
            },
            "view": {
                "type": "table",
                "title": title,
                "columns": [{"field": "x", "label": "X"}],
            },
        },
    )


def test_server_session_owns_history_after_bootstrap():
    store = SqliteSessionStore(":memory:")
    manager = SessionManager(store, recent_messages=4, relevant_history_messages=2)
    state = manager.get_or_create("s-1")

    incoming = make_input(
        "第三问",
        history=[
            HermesChatMessage(role="user", content="第一问"),
            HermesChatMessage(role="assistant", content="第一答"),
        ],
    )
    manager.bootstrap_history(state, incoming)
    manager.complete_turn(state, "第二问", "第二答")

    # Frontend later sends stale/different history. Once server state exists it
    # must not replace Python-owned conversation state.
    stale = make_input(
        "第三问",
        history=[HermesChatMessage(role="user", content="前端错误历史")],
    )
    manager.bootstrap_history(state, stale)

    selected = manager.select_history(state, "第三问")
    contents = [item.content for item in selected]
    assert "前端错误历史" not in contents
    assert "第二问" in contents
    assert "第二答" in contents


def test_artifact_turn_does_not_store_huge_dsl_in_conversation():
    store = SqliteSessionStore(":memory:")
    manager = SessionManager(store)
    state = manager.get_or_create("s-artifact")

    huge_dsl = json.dumps({"action": "create", "transform": "x" * 50000})
    manager.complete_turn(
        state,
        "创建报表",
        huge_dsl,
        run_id="run-1",
        artifact_id="artifact-1",
    )

    assert len(state.messages[-1].content) < 200
    assert "artifact-1" in state.messages[-1].content
    assert "x" * 100 not in state.messages[-1].content


def test_context_manager_keeps_selected_full_and_summarizes_other_blocks():
    store = SqliteSessionStore(":memory:")
    manager = SessionManager(store)
    context = ContextManager(
        manager,
        max_context_tokens=12000,
        max_dsl_tokens=2500,
        max_history_tokens=1500,
    )
    state = manager.get_or_create("s-context")

    blocks = [
        make_block("a", "持仓平均PE", transform_size=800),
        make_block("b", "组合久期", transform_size=800),
        make_block("c", "股票净敞口", transform_size=800),
        make_block("d", "行业配置", transform_size=800),
        make_block("e", "风险指标", transform_size=800),
    ]
    incoming = make_input("把当前PE表改成图", blocks, selected="a")

    prepared, report = context.prepare(state, incoming)

    assert len(prepared.currentDsls) == 5
    selected = next(item for item in prepared.currentDsls if item.blockId == "a")
    other = next(item for item in prepared.currentDsls if item.blockId == "e")

    selected_dsl = selected.dsl if isinstance(selected.dsl, dict) else selected.dsl.model_dump(exclude_none=True)
    other_dsl = other.dsl if isinstance(other.dsl, dict) else other.dsl.model_dump(exclude_none=True)

    assert "transform" in selected_dsl
    assert "transform" not in other_dsl
    assert report.full_dsl_blocks >= 1
    assert report.summarized_dsl_blocks >= 1



def test_context_manager_enforces_total_dynamic_budget():
    store = SqliteSessionStore(":memory:")
    manager = SessionManager(store, recent_messages=20, relevant_history_messages=0)
    context = ContextManager(
        manager,
        max_context_tokens=8000,
        max_dsl_tokens=2500,
        max_history_tokens=5000,
        reserved_prompt_tokens=3000,
    )
    state = manager.get_or_create("s-budget")
    for index in range(12):
        manager.complete_turn(
            state,
            f"用户历史 {index} " + ("问题" * 300),
            f"助手历史 {index} " + ("回答" * 300),
        )
    state.summary = "旧会话摘要" * 1200
    manager.store.put(state)

    incoming = make_input(
        "修改当前表",
        [make_block("a", "当前表", transform_size=1200)],
        selected="a",
    )

    prepared, report = context.prepare(state, incoming)

    assert report.total_estimated_tokens <= report.budget_tokens
    assert report.budget_tokens == 5000
    assert report.reserved_prompt_tokens == 3000
    assert report.dropped_history_messages > 0 or report.summary_truncated
    assert prepared.selectedBlockId == "a"
