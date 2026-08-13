from typing import Any, Dict, List, Literal, Optional
from pydantic import BaseModel, ConfigDict, Field

RunStatus = Literal[
    "queued",
    "running",
    "validating",
    "repairing",
    "completed",
    "failed",
    "expired",
]


class AbortSignal:
    def __init__(self, controller: "AbortController") -> None:
        self._controller = controller

    @property
    def aborted(self) -> bool:
        return self._controller.aborted


class AbortController:
    def __init__(self) -> None:
        self._aborted = False
        self.signal = AbortSignal(self)

    @property
    def aborted(self) -> bool:
        return self._aborted

    def abort(self) -> None:
        self._aborted = True


class RunRecord(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    id: str
    status: RunStatus
    request: Optional[Any] = None
    normalizedInput: Optional[Any] = Field(default=None, alias="normalized_input")
    finalWireText: Optional[str] = Field(default=None, alias="final_wire_text")
    errorCode: Optional[str] = Field(default=None, alias="error_code")
    eventBuffer: List[str] = Field(default_factory=list, alias="event_buffer")
    attemptCount: int = Field(default=0, alias="attempt_count")
    repairAttempts: int = Field(default=0, alias="repair_attempts")
    createdAt: float = Field(alias="created_at")
    startedAt: Optional[float] = Field(default=None, alias="started_at")
    completedAt: Optional[float] = Field(default=None, alias="completed_at")
    expiresAt: float = Field(alias="expires_at")
    controller: Optional[AbortController] = None

    def __getitem__(self, item: str) -> Any:
        return getattr(self, item)

    @property
    def created_at(self) -> float:
        return self.createdAt

    @property
    def expires_at(self) -> float:
        return self.expiresAt

    @property
    def started_at(self) -> Optional[float]:
        return self.startedAt

    @property
    def completed_at(self) -> Optional[float]:
        return self.completedAt

    @property
    def event_buffer(self) -> List[str]:
        return self.eventBuffer

    @property
    def attempt_count(self) -> int:
        return self.attemptCount

    @property
    def repair_attempts(self) -> int:
        return self.repairAttempts

    @property
    def final_wire_text(self) -> Optional[str]:
        return self.finalWireText

    @property
    def error_code(self) -> Optional[str]:
        return self.errorCode

    @property
    def normalized_input(self) -> Optional[Any]:
        return self.normalizedInput


class ClaimOutcome(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    outcome: Literal["claimed", "replay", "streaming", "not_found"]
    record: Optional[RunRecord] = None

    def __getitem__(self, item: str) -> Any:
        return getattr(self, item)
