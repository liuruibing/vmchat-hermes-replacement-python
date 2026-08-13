import asyncio
import time
import uuid
from typing import Any, Dict, List, Literal, Optional, Union
from pydantic import BaseModel, Field
from app.runs.run_types import AbortController, ClaimOutcome, RunRecord, RunStatus


class RunStoreOptions(BaseModel):
    maxStoredRuns: Optional[int] = Field(default=100, alias="max_stored_runs")
    defaultTtlMs: Optional[int] = Field(default=600000, alias="default_ttl_ms")


class RunStore:
    def __init__(
        self,
        options: Optional[Union[RunStoreOptions, Dict[str, Any]]] = None,
        max_stored_runs: int = 100,
        default_ttl_ms: int = 600000,
        maxStoredRuns: Optional[int] = None,
        defaultTtlMs: Optional[int] = None,
    ) -> None:
        opts_dict: Dict[str, Any] = {}
        if isinstance(options, BaseModel):
            opts_dict = options.model_dump()
        elif isinstance(options, dict):
            opts_dict = options

        m_runs = max_stored_runs
        if maxStoredRuns is not None:
            m_runs = maxStoredRuns
        elif "maxStoredRuns" in opts_dict and opts_dict["maxStoredRuns"] is not None:
            m_runs = opts_dict["maxStoredRuns"]
        elif "max_stored_runs" in opts_dict and opts_dict["max_stored_runs"] is not None:
            m_runs = opts_dict["max_stored_runs"]

        d_ttl = default_ttl_ms
        if defaultTtlMs is not None:
            d_ttl = defaultTtlMs
        elif "defaultTtlMs" in opts_dict and opts_dict["defaultTtlMs"] is not None:
            d_ttl = opts_dict["defaultTtlMs"]
        elif "default_ttl_ms" in opts_dict and opts_dict["default_ttl_ms"] is not None:
            d_ttl = opts_dict["default_ttl_ms"]

        self.max_stored_runs = m_runs
        self.maxStoredRuns = m_runs
        self.default_ttl_ms = d_ttl
        self.defaultTtlMs = d_ttl

        self.store: Dict[str, RunRecord] = {}
        self.cleanup_timer: Optional[asyncio.Task] = None
        self.cleanupTimer = None

        try:
            loop = asyncio.get_running_loop()
            if loop and loop.is_running():
                self.cleanup_timer = loop.create_task(self._periodic_cleanup())
                self.cleanupTimer = self.cleanup_timer
        except RuntimeError:
            pass

    async def _periodic_cleanup(self) -> None:
        try:
            while True:
                await asyncio.sleep(60)
                self.cleanup()
        except asyncio.CancelledError:
            pass

    def destroy(self) -> None:
        if self.cleanup_timer and not self.cleanup_timer.done():
            self.cleanup_timer.cancel()

    def cleanup(self) -> int:
        now = time.time() * 1000
        cleaned = 0
        expired_ids: List[str] = []

        for id_, record in list(self.store.items()):
            if record.expiresAt <= now:
                if (
                    record.controller
                    and record.status not in ("completed", "failed", "expired")
                ):
                    record.controller.abort()
                record.status = "expired"
                expired_ids.append(id_)
                cleaned += 1

        for id_ in expired_ids:
            self.store.pop(id_, None)

        return cleaned

    def create(
        self,
        request: Optional[Any] = None,
        normalized_input: Optional[Any] = None,
        ttl_ms: Optional[int] = None,
        normalizedInput: Optional[Any] = None,
        ttlMs: Optional[int] = None,
    ) -> RunRecord:
        self.cleanup()

        if len(self.store) >= self.max_stored_runs:
            raise RuntimeError("RUN_STORE_FULL: Run store capacity reached")

        id_ = f"run-{uuid.uuid4()}"
        now = time.time() * 1000
        ttl = ttl_ms if ttl_ms is not None else (ttlMs if ttlMs is not None else self.default_ttl_ms)
        expires_at = now + ttl
        n_input = normalized_input if normalized_input is not None else normalizedInput

        record = RunRecord(
            id=id_,
            status="queued",
            eventBuffer=[],
            attemptCount=0,
            repairAttempts=0,
            createdAt=now,
            expiresAt=expires_at,
            request=request,
            normalizedInput=n_input,
        )

        self.store[id_] = record
        return record

    def get(self, id: str) -> Optional[RunRecord]:
        record = self.store.get(id)
        if not record:
            return None
        if record.expiresAt <= time.time() * 1000 or record.status == "expired":
            self.store.pop(id, None)
            return None
        return record

    def claim(self, id: str) -> ClaimOutcome:
        record = self.get(id)
        if not record:
            return ClaimOutcome(outcome="not_found")

        if record.status in ("completed", "failed"):
            return ClaimOutcome(outcome="replay", record=record)

        if record.status in ("running", "validating", "repairing"):
            return ClaimOutcome(outcome="streaming", record=record)

        if record.status == "queued":
            record.status = "running"
            record.startedAt = time.time() * 1000
            record.controller = AbortController()
            return ClaimOutcome(outcome="claimed", record=record)

        return ClaimOutcome(outcome="not_found")

    def set_phase(self, id: str, phase: Literal["running", "validating", "repairing"]) -> None:
        record = self.get(id)
        if not record:
            raise RuntimeError(f"RUN_NOT_FOUND: Run {id} not found")

        active_statuses = ("running", "validating", "repairing")
        if record.status not in active_statuses:
            raise RuntimeError(
                f"ILLEGAL_RUN_TRANSITION: Cannot transition run {id} from {record.status} to {phase}"
            )

        record.status = phase

    setPhase = set_phase

    def record_attempt(self, id: str, is_repair: bool = False, isRepair: Optional[bool] = None) -> None:
        flag = is_repair if isRepair is None else isRepair
        record = self.get(id)
        if record:
            record.attemptCount += 1
            if flag:
                record.repairAttempts += 1

    recordAttempt = record_attempt

    def append_event(self, id: str, sse_line: str = "", sseLine: Optional[str] = None) -> None:
        line = sse_line if sseLine is None else sseLine
        record = self.get(id)
        if record:
            record.eventBuffer.append(line)

    appendEvent = append_event

    def complete(self, id: str, final_wire_text: str = "", finalWireText: Optional[str] = None) -> None:
        text = final_wire_text if finalWireText is None else finalWireText
        record = self.get(id)
        if not record:
            raise RuntimeError(f"RUN_NOT_FOUND: Run {id} not found")

        active_statuses = ("running", "validating", "repairing")
        if record.status not in active_statuses:
            raise RuntimeError(
                f"ILLEGAL_RUN_TRANSITION: Cannot transition run {id} from {record.status} to completed"
            )

        now = time.time() * 1000
        record.status = "completed"
        record.completedAt = now
        record.finalWireText = text
        record.request = None
        record.normalizedInput = None
        record.expiresAt = now + self.default_ttl_ms

    def fail(self, id: str, error_code: str = "", errorCode: Optional[str] = None) -> None:
        code = error_code if errorCode is None else errorCode
        record = self.get(id)
        if not record:
            raise RuntimeError(f"RUN_NOT_FOUND: Run {id} not found")

        cancellable_statuses = ("queued", "running", "validating", "repairing")
        if record.status not in cancellable_statuses:
            raise RuntimeError(
                f"ILLEGAL_RUN_TRANSITION: Cannot transition run {id} from {record.status} to failed"
            )

        now = time.time() * 1000
        record.status = "failed"
        record.completedAt = now
        record.errorCode = code
        record.request = None
        record.normalizedInput = None
        record.expiresAt = now + self.default_ttl_ms

    def expire(self, id: str) -> None:
        record = self.store.get(id)
        if not record:
            return

        if (
            record.controller
            and record.status not in ("completed", "failed", "expired")
        ):
            record.controller.abort()
        record.status = "expired"
        self.store.pop(id, None)
