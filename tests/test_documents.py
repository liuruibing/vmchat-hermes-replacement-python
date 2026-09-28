from fastapi.testclient import TestClient

from app.compatibility.hermes_request import (
    GlobalQueryParameters,
    VmChatInput,
    normalize_create_run_request,
    normalize_vm_chat_input,
)
from app.main import create_app
from app.workflow.engine import WorkflowContext
from app.workflow.graphs.mandate_risk import _resolve_uploaded_document


class MockResourceLoader:
    def is_ready(self):
        return True

    def get_resources(self):
        return {}

    async def load(self):
        return None


class DummyProvider:
    pass


def _pdf_bytes() -> bytes:
    content = (
        b"BT\n"
        b"/F1 12 Tf\n"
        b"72 720 Td\n"
        b"(Proper active management and low Tracking Error.) Tj\n"
        b"0 -20 Td\n"
        b"(Gain stable dividend yield and total return in excess of benchmark.) Tj\n"
        b"ET\n"
    )
    objects = [
        b"1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n",
        b"2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n",
        b"3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
        b"/Resources << /Font << /F1 5 0 R >> >> /Contents 4 0 R >>\nendobj\n",
        b"4 0 obj\n<< /Length " + str(len(content)).encode("ascii") + b" >>\nstream\n"
        + content
        + b"endstream\nendobj\n",
        b"5 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>\nendobj\n",
    ]

    payload = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets = [0]
    for obj in objects:
        offsets.append(len(payload))
        payload.extend(obj)

    xref_offset = len(payload)
    payload.extend(f"xref\n0 {len(objects) + 1}\n".encode("ascii"))
    payload.extend(b"0000000000 65535 f \n")
    for offset in offsets[1:]:
        payload.extend(f"{offset:010d} 00000 n \n".encode("ascii"))
    payload.extend(
        (
            f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\n"
            f"startxref\n{xref_offset}\n%%EOF\n"
        ).encode("ascii")
    )
    return bytes(payload)


def test_create_run_contract_accepts_document_references():
    request = normalize_create_run_request({
        "model": "deepseek-v4-flash",
        "session_id": "session-1",
        "agent_id": "mandate-risk-ai",
        "role_id": "risk-analyst",
        "documents": [
            "doc_abc123",
            {"document_id": "doc_abc123"},
            {"documentId": "doc_def456"},
        ],
        "input": [{"role": "user", "content": "分析这个 PDF"}],
    })
    assert request.documents == ["doc_abc123", "doc_def456"]

    vm_input = normalize_vm_chat_input(request)
    assert vm_input.documentIds == ["doc_abc123", "doc_def456"]
    assert vm_input.agentId == "mandate-risk-ai"
    assert vm_input.roleId == "risk-analyst"


def test_document_upload_parses_pdf_and_hides_server_paths():
    app = create_app({
        "resource_loader": MockResourceLoader(),
        "provider": DummyProvider(),
    })
    with TestClient(app) as client:
        response = client.post(
            "/v1/documents",
            files={"file": ("mandate.pdf", _pdf_bytes(), "application/pdf")},
        )

    assert response.status_code == 201, response.text
    document = response.json()["document"]
    assert document["document_id"].startswith("doc_")
    assert document["filename"] == "mandate.pdf"
    assert document["mime_type"] == "application/pdf"
    assert document["page_count"] == 1
    assert document["status"] == "ready"
    assert len(document["sha256"]) == 64
    assert "file_path" not in document
    assert "parsed_path" not in document


def test_document_upload_rejects_non_pdf():
    app = create_app({
        "resource_loader": MockResourceLoader(),
        "provider": DummyProvider(),
    })
    with TestClient(app) as client:
        response = client.post(
            "/v1/documents",
            files={"file": ("mandate.txt", b"not a pdf", "text/plain")},
        )

    assert response.status_code == 400
    assert "UNSUPPORTED_DOCUMENT_TYPE" in response.json()["error"]


def test_mandate_workflow_resolves_uploaded_document_by_id():
    input_val = VmChatInput(
        userMessage="分析上传文件",
        globalQueryParameters=GlobalQueryParameters(),
        agentId="mandate-risk-ai",
        roleId="risk-analyst",
        documentIds=["doc_test"],
    )
    loaded = []

    def load_document(document_id):
        loaded.append(document_id)
        return {
            "filename": "mandate.pdf",
            "text": "[Page 1]\nProper active management and low Tracking Error.",
        }

    context = WorkflowContext(
        input_val=input_val,
        provider=DummyProvider(),
        agent_id="mandate-risk-ai",
        role_id="risk-analyst",
        document_ids=["doc_test"],
        document_loader=load_document,
    )

    name, text = _resolve_uploaded_document(context)
    assert loaded == ["doc_test"]
    assert name == "mandate.pdf"
    assert "low Tracking Error" in text
