# ==============================================================================
# 文件：app/workflow/registry.py
# 文件作用：保存工作流 id 与实现对象的对应关系，供 Engine 查找。
# 全局位置：legacy.py 创建默认实例 → 本文件登记 → WorkflowEngine 按 id 取出实例。
# 谁调用它：默认注册函数及运行时注入代码写入目录，Engine 和查询接口读取目录。
# 输入：实现了 id/stream 约定的工作流对象，或要查找的工作流 id。
# 输出：对应的工作流对象、id 列表，或重复/未知 id 等明确异常。
# 主要流程：register 新增 → replace 替换 → get/require 查找 → list_ids 列出可用流程。
# 前端类比：类似 Map<string, Workflow>，key 是 Agent 配置中的 workflow 名称。
# 边界：登记和查找都不会执行图、调用模型或发送 SSE。
# 阅读入口：先看 register() 和 require()，再看 Engine 如何使用 require()。
# ==============================================================================

from __future__ import annotations

from typing import Dict, Iterable, List, Optional

from app.workflow.engine import WorkflowProtocol


class WorkflowRegistry:
    def __init__(self, workflows: Optional[Iterable[WorkflowProtocol]] = None) -> None:
        # Iterable 表示可遍历的一组对象，不要求调用方一定传 list。
        self._workflows: Dict[str, WorkflowProtocol] = {}
        for workflow in workflows or []:
            self.register(workflow)

    def register(self, workflow: WorkflowProtocol) -> None:
        # getattr(obj, name, default) 类似读取可选属性；strip 去掉 id 两端的空白。
        workflow_id = str(getattr(workflow, "id", "") or "").strip()
        if not workflow_id:
            raise ValueError("INVALID_WORKFLOW: workflow.id is required")
        if workflow_id in self._workflows:
            raise ValueError(f"DUPLICATE_WORKFLOW: {workflow_id}")
        self._workflows[workflow_id] = workflow

    def replace(self, workflow: WorkflowProtocol) -> None:
        # register 拒绝重复 id；replace 允许覆盖，便于运行时注入或替换某个实现。
        workflow_id = str(getattr(workflow, "id", "") or "").strip()
        if not workflow_id:
            raise ValueError("INVALID_WORKFLOW: workflow.id is required")
        self._workflows[workflow_id] = workflow

    def get(self, workflow_id: str) -> Optional[WorkflowProtocol]:
        return self._workflows.get(str(workflow_id or "").strip())

    def require(self, workflow_id: str) -> WorkflowProtocol:
        # get 可以返回 None；require 要求一定找到，否则交给上层转成明确的请求错误。
        workflow = self.get(workflow_id)
        if workflow is None:
            raise ValueError(f"UNKNOWN_WORKFLOW: {workflow_id}")
        return workflow

    def list_ids(self) -> List[str]:
        return sorted(self._workflows.keys())
