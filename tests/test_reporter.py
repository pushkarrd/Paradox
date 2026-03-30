import json

import reporter


def test_generate_report_writes_incident_json(tmp_path, monkeypatch):
    incident_dir = tmp_path / "incidents"
    monkeypatch.setattr(reporter, "INCIDENT_DIR", str(incident_dir))

    suspect = tmp_path / "suspect.bin"
    trusted = tmp_path / "trusted.bin"
    suspect.write_bytes(b"malicious")
    trusted.write_bytes(b"trusted")

    pipeline_result = {
        "trust_score": 20,
        "verdict": "COMPROMISED",
        "crack_type": "hook",
        "severity": "High",
        "diffs": [{"offset": "0x10"}],
        "size_delta": 4,
        "suspect_binary": str(suspect),
        "trusted_binary": str(trusted),
    }

    report = reporter.generate_report(pipeline_result)

    assert report["binary"] == str(suspect)
    assert report["verdict"] == "COMPROMISED"
    assert report["diff_count"] == 1
    assert report["offsets"] == ["0x10"]

    files = list(incident_dir.glob("incident_*.json"))
    assert files, "Incident report file was not created"

    loaded = json.loads(files[0].read_text(encoding="utf-8"))
    assert loaded["verdict"] == "COMPROMISED"
    assert loaded["binary"] == str(suspect)
