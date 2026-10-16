from __future__ import annotations

from typing import Any, Dict, List, Optional, TypedDict


class XianyuCsGraphState(TypedDict, total=False):
    # 会话与买家区分标识
    session_id: str
    buyer_id: str
    product_id: str

    # 用户输入与多轮对话记忆
    query: str
    history: List[Dict[str, str]]

    # 商品属性与技术知识库（Grounding）
    product_title: str
    product_price: float
    product_readme: str
    delivery_info: str

    # 意图路由结果
    intent: str  # tech_faq | bargain | delivery_faq | after_sales | greeting

    # 检索出的依据或业务约束策略
    grounding_notes: str

    # 最终客服应答内容
    reply: str
    usage: Dict[str, Any]
