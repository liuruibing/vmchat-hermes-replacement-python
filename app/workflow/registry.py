from __future__ import annotations

from typing import Dict, Iterable, List, Optional

from app.workflow.engine import WorkflowProtocol


class WorkflowRegistry:
    def __init__(self, workflows: Optional[Iterable[WorkflowProtocol]] = None) -> None:
        self._workflows: Dict[str, WorkflowProtocol] = {}
        for workflow in workflows or []:
            self.register(workflow)

    def register(self, workflow: WorkflowProtocol) -> None:
        workflow_id = str(getattr(workflow, "id", "") or "").strip()
        if not workflow_id:
            raise ValueError("INVALID_WORKFLOW: workflow.id is required")
        if workflow_id in self._workflows:
            raise ValueError(f"DUPLICATE_WORKFLOW: {workflow_id}")
        self._workflows[workflow_id] = workflow

    def replace(self, workflow: WorkflowProtocol) -> None:
        workflow_id = str(getattr(workflow, "id", "") or "").strip()
        if not workflow_id:
            raise ValueError("INVALID_WORKFLOW: workflow.id is required")
        self._workflows[workflow_id] = workflow

    def get(self, workflow_id: str) -> Optional[WorkflowProtocol]:
        return self._workflows.get(str(workflow_id or "").strip())

    def require(self, workflow_id: str) -> WorkflowProtocol:
        workflow = self.get(workflow_id)
        if workflow is None:
            raise ValueError(f"UNKNOWN_WORKFLOW: {workflow_id}")
        return workflow

    def list_ids(self) -> List[str]:
        return sorted(self._workflows.keys())
