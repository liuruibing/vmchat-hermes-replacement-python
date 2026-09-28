import base64

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


PDF_BASE64 = (
    "JVBERi0xLjMKJZOMi54gUmVwb3J0TGFiIEdlbmVyYXRlZCBQREYgZG9jdW1lbnQgKG9wZW5zb3VyY2UpCjEgMCBvYmoKPDwKL0YxIDIgMCBSCj4+CmVuZG9iagoyIDAgb2JqCjw8Ci9CYXNlRm9udCAvSGVsdmV0aWNhIC9FbmNvZGluZyAvV2luQW5zaUVuY29kaW5nIC9OYW1lIC9GMSAvU3VidHlwZSAvVHlwZTEgL1R5cGUgL0ZvbnQKPj4KZW5kb2JqCjMgMCBvYmoKPDwKL0NvbnRlbnRzIDcgMCBSIC9NZWRpYUJveCBbIDAgMCA2MTIgNzkyIF0gL1BhcmVudCA2IDAgUiAvUmVzb3VyY2VzIDw8Ci9Gb250IDEgMCBSIC9Qcm9jU2V0IFsgL1BERiAvVGV4dCAvSW1hZUIgL0ltYWdlQyAvSW1hZ2VJIF0KPj4gL1JvdGF0ZSAwIC9UcmFucyA8PAoKPj4gCiAgL1R5cGUgL1BhZ2UKPj4KZW5kb2JqCjQgMCBvYmoKPDwKL1BhZ2VNb2RlIC9Vc2VOb25lIC9QYWdlcyA2IDAgUiAvVHlwZSAvQ2F0YWxvZwo+PgplbmRvYmoKNSAwIG9iago8PAovQXV0aG9yIChhbm9ueW1vdXMpIC9DcmVhdGlvbkRhdGUgKEQ6MjAyNjA5MjgwNjE1NTcrMDAnMDAnKSAvQ3JlYXRvciAoYW5vbnltb3VzKSAvS2V5d29yZHMgKCkgL01vZERhdGUgKEQ6MjAyNjA5MjgwNjE1NTcrMDAnMDAnKSAvUHJvZHVjZXIgKFJlcG9ydExhYiBQREYgTGlicmFyeSAtIFwob3BlbnNvdXJjZVwpKSAKICAvU3ViamVjdCAodW5zcGVjaWZpZWQpIC9UaXRsZSAodW50aXRsZWQpIC9UcmFwcGVkIC9GYWxzZQo+PgplbmRvYmoKNiAwIG9iago8PAovQ291bnQgMSAvS2lkcyBbIDMgMCBSIF0gL1R5cGUgL1BhZ2VzCj4+CmVuZG9iago3IDAgb2JqCjw8Ci9GaWx0ZXIgWyAvQVNDSUk4NURlY29kZSAvRmxhdGVEZWNvZGUgXSAvTGVuZ3RoIDIwNQo+PgpzdHJlYW0KR2FyVzFZbXVENihrZCspaV5TJlU4a0BAM2QpRUhwMENWbmhZWDJSYztjMkZILyJzIl0tPyNJL1deL0hHQ2U8N2ZQSF1ARFk2J11lOzwwXlAzLWUoMU1eJXRLSkFUQGg9WVc+RmVaJSxOVDFXLD9RU2ZSXDZuaCVsTkovMG5tb2ZbJlArU2NyUCRHSDY7LzNeaW89Y1kiMDFHVyxxZ1FpTjpBVS8pLkEuNFNpI2ZqUSVVYTg1NzpENidNTDp0LFdQMlotO2ZjMFsuNVArfj5lbmRzdHJlYW0KZW5kb2JqCnhyZWYKMCA4CjAwMDAwMDAwMDAgNjU1MzUgZiAKMDAwMDAwMDA2MSAwMDAwMCBuIAowMDAwMDAwMDkyIDAwMDAwIG4gCjAwMDAwMDAxOTkgMDAwMDAgbiAKMDAwMDAwMDM5MiAwMDAwMCBuIAowMDAwMDAwNDYwIDAwMDAwIG4gCjAwMDAwMDA3MjEgMDAwMDAgbiAKMDAwMDAwMDc4MCAwMDAwMCBuIAp0cmFpbGVyCjw8Ci9JRCAKWzwxZWUwMjZmZDY5ZDVmNjIzODYzNjg0NjdlZGI4NWFiYz48MWVlMDI2ZmQ2OWQ1ZjYyMzg2MzY4NDY3ZWRiODVhYmM+XQolIFJlcG9ydExhYiBnZW5lcmF0ZWQgUERGIGRvY3VtZW50IC0tIGRpZ2VzdCAob3BlbnNvdXJjZSkKCi9JbmZvIDUgMCBSCi9Sb290IDQgMCBSCi9TaXplIDgKPj4Kc3RhcnR4cmVmCjEwNzUKJSVFT0YK"
)


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
    return base64.b64decode(PDF_BASE64)


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

    assert response.status_code == 201
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
