from typing import Any, Literal, Optional, Union
from pydantic import BaseModel, Field

from app.compatibility.hermes_request import VmReportDsl


class ValidationIssue(BaseModel):
    code: str
    path: str
    message: str


class ValidationSuccess(BaseModel):
    ok: Literal[True] = True
    dsls: list[VmReportDsl] = Field(default_factory=list)


class ValidationFailure(BaseModel):
    ok: Literal[False] = False
    errors: list[ValidationIssue] = Field(default_factory=list)


ValidationResult = Union[ValidationSuccess, ValidationFailure]


class VmChatRunError(Exception):
    def __init__(self, code: str, public_message: str, cause: Optional[Any] = None) -> None:
        super().__init__(f"[{code}] {public_message}")
        self.name = "VmChatRunError"
        self.code = code
        self.public_message = public_message
        self.publicMessage = public_message
        self.cause = cause
