import asyncio
from app.workflow.graphs.xianyu_cs_graph import compiled_xianyu_graph

async def test_langgraph_flow():
    print("=== [测试 1] 买家 A 第 1 轮咨询：Windows 安装与教程 ===")
    session_a = "xy_buyerA_rea"
    thread_config_a = {"configurable": {"thread_id": session_a}}

    input_1 = {
        "session_id": session_a,
        "buyer_id": "buyerA",
        "product_id": "prod-rea",
        "query": "我是 Windows 电脑小白，拍下后不会装怎么办？提供技术指导吗？",
        "history": [],
        "product_title": "REA 自动化逆向工程源码",
        "product_price": 19.9,
        "product_readme": "支持 Windows, Mac, Linux 跨平台运行。安装依赖只需 npm install 或 bun install。支持 Docker 一键部署：docker run -d rea。",
        "delivery_info": "拍下后系统自动秒发提货卡",
    }

    res_1 = await compiled_xianyu_graph.ainvoke(input_1, config=thread_config_a)
    print("✓ 买家 A 意图识别:", res_1.get("intent"))
    print("✓ 客服第 1 轮回复:", res_1.get("reply"))

    print("\n=== [测试 2] 买家 A 第 2 轮连续追问：Docker 与 换电脑 ===")
    state_a = await compiled_xianyu_graph.aget_state(thread_config_a)
    input_2 = {
        "session_id": session_a,
        "buyer_id": "buyerA",
        "product_id": "prod-rea",
        "query": "那支持 Docker 吗？如果我换了电脑还要重新买吗？",
        "history": state_a.values.get("history", []),
        "product_title": "REA 自动化逆向工程源码",
        "product_price": 19.9,
        "product_readme": "支持 Windows, Mac, Linux 跨平台运行。安装依赖只需 npm install 或 bun install。支持 Docker 一键部署：docker run -d rea。",
    }

    res_2 = await compiled_xianyu_graph.ainvoke(input_2, config=thread_config_a)
    print("✓ 买家 A 第 2 轮意图识别:", res_2.get("intent"))
    print("✓ 客服第 2 轮回复 (上下文接续):", res_2.get("reply"))
    print("✓ 买家 A 累积上下文轮数:", len(res_2.get("history", [])))

    print("\n=== [测试 3] 买家 B 新会话：砍价与底价问询 (会话隔离验证) ===")
    session_b = "xy_buyerB_rea"
    thread_config_b = {"configurable": {"thread_id": session_b}}

    input_b = {
        "session_id": session_b,
        "buyer_id": "buyerB",
        "product_id": "prod-rea",
        "query": "老板，9.9包邮卖不卖？能少点吗？",
        "history": [],
        "product_title": "REA 自动化逆向工程源码",
        "product_price": 19.9,
        "product_readme": "支持全平台运行。",
    }

    res_b = await compiled_xianyu_graph.ainvoke(input_b, config=thread_config_b)
    print("✓ 买家 B 意图识别 (应为 bargain):", res_b.get("intent"))
    print("✓ 客服对买家 B 的回复 (议价策略):", res_b.get("reply"))
    print("✓ 买家 B 历史轮数 (应为独立会话):", len(res_b.get("history", [])))

asyncio.run(test_langgraph_flow())
