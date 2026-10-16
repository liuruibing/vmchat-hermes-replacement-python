from __future__ import annotations

import json
import logging
import re
import shutil
from typing import Any, Dict, List

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph

from app.workflow.graphs.xianyu_cs_state import XianyuCsGraphState

logger = logging.getLogger("xianyu-cs-graph")


# 1. 意图识别节点
def route_intent_node(state: XianyuCsGraphState) -> Dict[str, Any]:
    query = (state.get("query") or "").strip().lower()

    # 砍价意图
    bargain_words = ["便宜", "少点", "能少", "小刀", "优惠", "底价", "最低", "包邮吗", "包邮", "能便宜", "送我"]
    if any(w in query for w in bargain_words):
        return {"intent": "bargain"}

    # 发货/提货意图
    delivery_words = ["发货", "怎么发", "多久发", "秒发", "自动发", "网盘", "链接", "提取", "怎么给", "提货"]
    if any(w in query for w in delivery_words):
        return {"intent": "delivery_faq"}

    # 售后排错意图
    after_sales_words = ["报错", "失败", "跑不起来", "运行不了", "缺少", "error", "bug", "安装不上", "出问题", "无法启动"]
    if any(w in query for w in after_sales_words):
        return {"intent": "after_sales"}

    # 简单问候
    greeting_words = ["在吗", "你好", "有人吗", "在不在", "hi", "hello", "师傅", "老板"]
    if len(query) <= 6 and any(w in query for w in greeting_words):
        return {"intent": "greeting"}

    # 默认技术/功能/兼容性咨询
    return {"intent": "tech_faq"}


# 2. 意图分支策略处理节点
def handle_tech_faq(state: XianyuCsGraphState) -> Dict[str, Any]:
    readme = state.get("product_readme") or ""
    query = state.get("query") or ""
    
    # 简单相关性截取：查找包含买家关键字的 README 片段
    keywords = [w for w in ["win", "mac", "linux", "python", "node", "docker", "gpu", "显卡", "教程", "部署", "环境"] if w in query.lower()]
    extracted_snippet = ""
    if keywords and readme:
        lines = readme.splitlines()
        matched = []
        for i, line in enumerate(lines):
            if any(k in line.lower() for k in keywords):
                start = max(0, i - 2)
                end = min(len(lines), i + 4)
                matched.append("\n".join(lines[start:end]))
        if matched:
            extracted_snippet = "\n---\n".join(matched[:3])

    if not extracted_snippet and readme:
        extracted_snippet = readme[:1500]

    return {
        "grounding_notes": f"【技术参考依据】：\n{extracted_snippet or '本项目包含完整工程源码及详细环境安装文档。'}"
    }


def handle_bargain(state: XianyuCsGraphState) -> Dict[str, Any]:
    price = state.get("product_price", 9.9)
    return {
        "grounding_notes": f"【议价处理策略】：当前定价为 ¥{price} 元，已经是整理测试好的特惠成本价。请委婉告知本店已配置 24 小时全自动发货，随买随到账，附送完整保姆级教程与环境指导，不接受小刀，但保证物超所值！"
    }


def handle_delivery_faq(state: XianyuCsGraphState) -> Dict[str, Any]:
    return {
        "grounding_notes": "【发货说明依据】：本店接入了 7x24 小时无人值守全自动发货系统。买家拍下付款后 10 秒内，系统自动在聊天窗口发送专属提货卡片（含二维码直达与提取密码），买家扫码可在手机/电脑浏览器直接一键极速下载最新完整版 ZIP 压缩源码包，免除打不开 GitHub 的烦恼！"
    }


def handle_after_sales(state: XianyuCsGraphState) -> Dict[str, Any]:
    return {
        "grounding_notes": "【售后支持策略】：态度真诚负责，告知数字资料已包含完整源码与常见避坑指南。请买家把具体报错截图或命令发在聊天框，我们会第一时间协助排查调试，让买家安心。"
    }


def handle_greeting(state: XianyuCsGraphState) -> Dict[str, Any]:
    title = state.get("product_title", "该资料")
    return {
        "grounding_notes": f"【接待策略】：热情打招呼，告知【{title}】现货在售，系统已开启 24 小时自动秒发，询问买家有什么想了解的，或者喜欢可以直接拍下。"
    }


# 3. 提示词合成与大模型调用节点（带多轮会话记忆注入）
async def call_llm_node(state: XianyuCsGraphState) -> Dict[str, Any]:
    title = state.get("product_title") or "技术源码与资料包"
    price = state.get("product_price", 9.9)
    notes = state.get("grounding_notes") or ""
    query = state.get("query") or ""
    history = state.get("history") or []

    # 格式化多轮历史对话
    history_text = ""
    if history:
        h_lines = ["<chat_history>"]
        # 取最近 6 轮
        for item in history[-6:]:
            role = "买家" if item.get("role") in ["user", "buyer"] else "客服"
            h_lines.append(f"{role}: {item.get('content', '')}")
        h_lines.append("</chat_history>")
        history_text = "\n".join(h_lines)

    system_prompt = f"""你是一名性格热情、精通技术的闲鱼金牌客服。
你正在接待一位买家，买家正在咨询你店铺里的商品【{title}】（售价 ¥{price} 元）。

【业务事实依据】：
{notes}

【回复原则】：
1. 语言亲切自然，称呼买家为“亲”或“朋友”；
2. 结合【上下文对话历史】和【业务事实依据】精准回答买家当下的提问，不答非所问；
3. 如果买家提到了上一句话代词（如“这个”、“那配置呢”），根据历史上下文无缝承接；
4. 语言精简干练（控制在 100 字左右），并在末尾自然引导买家直接拍下；
5. 严禁引导加微信或站外联系，严禁包含违禁词。"""

    user_prompt = f"{history_text}\n\n买家最新发来: \"{query}\"\n请生成你的回复内容："

    # 调用本地 OMP 命令
    from app.workflow.graphs.simple_chat import _is_aborted
    import asyncio

    omp_exec = shutil.which("omp") or "/Users/liuruibing/.bun/bin/omp"
    try:
        proc = await asyncio.create_subprocess_exec(
            omp_exec,
            f"--system-prompt={system_prompt}",
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await proc.communicate(input=user_prompt.encode("utf-8"))
        reply_text = stdout.decode("utf-8").strip()
        if reply_text.startswith("Working..."):
            reply_text = reply_text.replace("Working...", "").strip()
        if not reply_text:
            reply_text = "亲，在的！拍下后系统 10 秒自动秒发最新完整 ZIP 源码包和保姆级运行教程，喜欢可直接拍下哦～"
    except Exception as exc:
        logger.warning("调用 OMP 失败，使用兜底回答: %s", exc)
        reply_text = "亲，在的！拍下后系统 10 秒自动秒发最新完整 ZIP 源码包和保姆级运行教程，喜欢可直接拍下哦～"

    # 更新历史记录
    new_history = list(history)
    new_history.append({"role": "user", "content": query})
    new_history.append({"role": "assistant", "content": reply_text})

    return {
        "reply": reply_text,
        "history": new_history,
    }


# 4. 构建 LangGraph 图
def build_xianyu_cs_graph() -> StateGraph:
    workflow = StateGraph(XianyuCsGraphState)

    # 注册节点
    workflow.add_node("route_intent", route_intent_node)
    workflow.add_node("handle_tech_faq", handle_tech_faq)
    workflow.add_node("handle_bargain", handle_bargain)
    workflow.add_node("handle_delivery_faq", handle_delivery_faq)
    workflow.add_node("handle_after_sales", handle_after_sales)
    workflow.add_node("handle_greeting", handle_greeting)
    workflow.add_node("call_llm", call_llm_node)

    # 起始连接
    workflow.add_edge(START, "route_intent")

    # 条件分支
    def intent_selector(state: XianyuCsGraphState) -> str:
        intent = state.get("intent", "tech_faq")
        mapping = {
            "tech_faq": "handle_tech_faq",
            "bargain": "handle_bargain",
            "delivery_faq": "handle_delivery_faq",
            "after_sales": "handle_after_sales",
            "greeting": "handle_greeting",
        }
        return mapping.get(intent, "handle_tech_faq")

    workflow.add_conditional_edges(
        "route_intent",
        intent_selector,
        {
            "handle_tech_faq": "handle_tech_faq",
            "handle_bargain": "handle_bargain",
            "handle_delivery_faq": "handle_delivery_faq",
            "handle_after_sales": "handle_after_sales",
            "handle_greeting": "handle_greeting",
        },
    )

    # 分支汇聚到模型调用
    for node_name in ["handle_tech_faq", "handle_bargain", "handle_delivery_faq", "handle_after_sales", "handle_greeting"]:
        workflow.add_edge(node_name, "call_llm")

    # 结束
    workflow.add_edge("call_llm", END)

    return workflow


# 编译后的单例执行图
compiled_xianyu_graph = build_xianyu_cs_graph().compile(checkpointer=InMemorySaver())
