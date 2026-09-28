from __future__ import annotations

from email.parser import BytesParser
from email.policy import default
from typing import Tuple


def parse_single_file_multipart(content_type: str, body: bytes, field_name: str = "file") -> Tuple[str, str, bytes]:
    """Parse one multipart file upload using the standard library.

    FastAPI/Starlette's request.form() requires python-multipart. The document
    endpoint intentionally keeps the runtime dependency surface small by
    accepting one file part and parsing it with the stdlib email package.
    """

    content_type = str(content_type or "").strip()
    if not content_type.lower().startswith("multipart/form-data"):
        raise ValueError("INVALID_MULTIPART: Content-Type must be multipart/form-data")
    if not body:
        raise ValueError("INVALID_MULTIPART: empty request body")

    message = BytesParser(policy=default).parsebytes(
        b"MIME-Version: 1.0\r\nContent-Type: "
        + content_type.encode("latin-1", "ignore")
        + b"\r\n\r\n"
        + body
    )
    if not message.is_multipart():
        raise ValueError("INVALID_MULTIPART: malformed multipart body")

    for part in message.iter_parts():
        disposition = part.get_content_disposition()
        name = part.get_param("name", header="content-disposition")
        filename = part.get_filename()
        if disposition != "form-data" or name != field_name or not filename:
            continue
        payload = part.get_payload(decode=True)
        if payload is None:
            payload = b""
        mime_type = str(part.get_content_type() or "application/octet-stream")
        return str(filename), mime_type, bytes(payload)

    raise ValueError(f"INVALID_MULTIPART: missing file field '{field_name}'")
