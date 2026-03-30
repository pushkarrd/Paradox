import importlib
import io
import json
import os
import sys
import types
from pathlib import Path

import pytest


def install_stub_modules():
    pipeline = types.ModuleType("pipeline")

    def run_pipeline(source, suspect, trusted):
        if not source or not suspect or not trusted:
            return {"error": "Missing required fields"}

        compromised = "fake_compiler.py" in os.path.basename(suspect) or "fake_compiler.py" in suspect
        if compromised:
            verdict = "COMPROMISED"
            score = 42
            crack_type = "appended"
            severity = "high"
            diffs = [{"offset": "0x0", "suspect_byte": "0x90", "trusted_byte": "0x48"}]
        else:
            verdict = "TRUSTED"
            score = 100
            crack_type = "none"
            severity = "low"
            diffs = []

        return {
            "trust_score": score,
            "verdict": verdict,
            "crack_type": crack_type,
            "severity": severity,
            "diffs": diffs,
        }

    pipeline.run_pipeline = run_pipeline

    responder = types.ModuleType("responder")

    def respond(pr):
        actions = ["incident_logged"]
        if pr.get("verdict") == "COMPROMISED":
            actions.insert(0, "quarantined")
        return actions

    responder.respond = respond

    reporter = types.ModuleType("reporter")

    def generate_report(pr):
        return {
            "timestamp": "123",
            "sha256": "abc",
            "diff_count": len(pr.get("diffs", [])),
        }

    reporter.generate_report = generate_report

    sys.modules["pipeline"] = pipeline
    sys.modules["responder"] = responder
    sys.modules["reporter"] = reporter


@pytest.fixture()
def client(tmp_path):
    install_stub_modules()

    repo_root = Path(__file__).resolve().parents[1]
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))

    import backend.app as app_module

    importlib.reload(app_module)

    app = app_module.app
    app.config.update(
        TESTING=True,
        INCIDENTS_DIR=str(tmp_path / "incidents"),
        WHITELIST_PATH=str(tmp_path / "whitelist.json"),
        UPLOAD_DIR=str(tmp_path / "uploads"),
    )

    return app.test_client()


def test_status(client):
    response = client.get("/api/status")
    data = response.get_json()

    assert response.status_code == 200
    assert data["status"] == "ok"
    assert "version" in data
    assert "uptime" in data


def test_validate_missing_fields(client):
    response = client.post("/api/validate", json={})
    data = response.get_json()

    assert response.status_code == 400
    assert "error" in data


def test_validate_compromised_flow(client):
    payload = {
        "source_path": "samples/clean.c",
        "suspect_compiler": "backend/fake_compiler.py",
        "trusted_compiler": "/usr/bin/gcc",
    }
    response = client.post("/api/validate", json=payload)
    data = response.get_json()

    assert response.status_code == 200
    assert data["verdict"] == "COMPROMISED"
    assert data["crack_type"] == "appended"
    assert data["severity"] == "high"
    assert data["error"] is None


def test_incidents_and_report(client):
    inc_dir = Path(client.application.config["INCIDENTS_DIR"])
    inc_dir.mkdir(parents=True, exist_ok=True)

    incident = {
        "timestamp": "123",
        "sha256": "abc",
        "verdict": "COMPROMISED",
        "crack_type": "appended",
        "score": 42,
    }

    with open(inc_dir / "123.json", "w", encoding="utf-8") as handle:
        json.dump(incident, handle)

    list_response = client.get("/api/incidents")
    list_data = list_response.get_json()

    assert list_response.status_code == 200
    assert any(item.get("timestamp") == "123" for item in list_data)

    report_response = client.get("/api/report/123")
    report_data = report_response.get_json()

    assert report_response.status_code == 200
    assert report_data["sha256"] == "abc"


def test_whitelist(client):
    whitelist_path = Path(client.application.config["WHITELIST_PATH"])
    whitelist = [{"path": "samples/clean.c", "sha256": "abc", "approved": True}]

    with open(whitelist_path, "w", encoding="utf-8") as handle:
        json.dump(whitelist, handle)

    response = client.get("/api/whitelist")
    data = response.get_json()

    assert response.status_code == 200
    assert data == whitelist


def test_upload(client):
    data = {"source": (io.BytesIO(b"int main(void) { return 0; }"), "hello.c")}

    response = client.post("/api/upload", data=data, content_type="multipart/form-data")
    body = response.get_json()

    assert response.status_code == 200
    assert body["filename"] == "hello.c"
    assert os.path.exists(body["saved_path"])
