import inspect
import json
from typing import Any, Dict, Generator, Literal, Optional, Protocol, Union, runtime_checkable
from pydantic import BaseModel, Field


class MessageDeltaEvent(BaseModel):
    event: Literal["message.delta"] = "message.delta"
    delta: str


class ReasoningDeltaEvent(BaseModel):
    event: Literal["reasoning.delta"] = "reasoning.delta"
    delta: str
    sequence: int


class ReasoningDoneEvent(BaseModel):
    event: Literal["reasoning.done"] = "reasoning.done"


class RunCompletedEvent(BaseModel):
    event: Literal["run.completed"] = "run.completed"
    output: str
    usage: Optional[Dict[str, Any]] = Field(default_factory=dict)


class RunFailedEvent(BaseModel):
    event: Literal["run.failed"] = "run.failed"
    error: str


HermesSseEvent = Union[
    MessageDeltaEvent,
    ReasoningDeltaEvent,
    ReasoningDoneEvent,
    RunCompletedEvent,
    RunFailedEvent,
]

def serialize_sse_event(event: Union[HermesSseEvent, Dict[str, Any]]) -> str:
    """Serializes a HermesSseEvent or dict into an SSE data line using json.dumps."""
    if isinstance(event, BaseModel):
        data = event.model_dump(exclude_none=True)
    elif isinstance(event, dict):
        data = event
    else:
        raise TypeError(f"Unsupported event type: {type(event)}")
    return f"data: {json.dumps(data, separators=(',', ':'), ensure_ascii=False)}\n\n"



# Alias for JS camelCase compatibility
serializeSseEvent = serialize_sse_event


def code_point_chunks(text: str, chunk_size: int = 256) -> Generator[str, None, None]:
    """Yields chunks of text sliced by unicode code points natively in Python."""
    if not text:
        return
    for i in range(0, len(text), chunk_size):
        yield text[i : i + chunk_size]


# Alias for JS camelCase compatibility
codePointChunks = code_point_chunks


@runtime_checkable
class AbortSignal(Protocol):
    aborted: bool


@runtime_checkable
class StreamWriter(Protocol):
    signal: Optional[AbortSignal]

    def write(self, data: str) -> bool:
        ...

    async def drain(self) -> None:
        ...

    def is_destroyed(self) -> bool:
        ...


class ClientDisconnectedError(Exception):
    """Raised when stream writer is aborted or destroyed."""
    pass


def check_state(writer: Any) -> None:
    signal = getattr(writer, "signal", None)
    if signal is not None and getattr(signal, "aborted", False):
        raise ClientDisconnectedError("CLIENT_DISCONNECTED: Connection closed or stream aborted")

    is_destroyed = getattr(writer, "is_destroyed", None)
    if is_destroyed is not None:
        destroyed = is_destroyed() if callable(is_destroyed) else is_destroyed
        if destroyed:
            raise ClientDisconnectedError("CLIENT_DISCONNECTED: Connection closed or stream aborted")


async def write_final_result(
    writer: Any,
    final_text: str,
    usage: Optional[Dict[str, Any]] = None,
    chunk_size: int = 256,
) -> None:
    """Legacy pseudo-streaming: slices pre-computed finalText into message.delta chunks.
    Kept for backward compatibility; new code path uses streamVmChat + real streaming.
    """
    for chunk in code_point_chunks(final_text, chunk_size):
        check_state(writer)
        sse_line = serialize_sse_event(MessageDeltaEvent(delta=chunk))

        write_res = writer.write(sse_line)
        if inspect.isawaitable(write_res):
            ok = await write_res
        else:
            ok = write_res

        if not ok:
            check_state(writer)
            drain = getattr(writer, "drain", None)
            if drain is not None and callable(drain):
                drain_res = drain()
                if inspect.isawaitable(drain_res):
                    await drain_res

    check_state(writer)
    completed_event = RunCompletedEvent(
        output=final_text,
        usage=usage if usage is not None else {},
    )
    completed_line = serialize_sse_event(completed_event)
    write_res = writer.write(completed_line)
    if inspect.isawaitable(write_res):
        ok = await write_res
    else:
        ok = write_res

    if not ok:
        check_state(writer)
        drain = getattr(writer, "drain", None)
        if drain is not None and callable(drain):
            drain_res = drain()
            if inspect.isawaitable(drain_res):
                await drain_res


# Alias for JS camelCase compatibility
writeFinalResult = write_final_result
