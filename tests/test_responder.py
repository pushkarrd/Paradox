import json

import reporter
import responder


def _pipeline_result(suspect, trusted, verdict, crack_type, diffs=None):
    return {
        "trust_score": 100 if verdict == "TRUSTED" else 30,
        "verdict": verdict,
        "crack_type": crack_type,
        "severity": "High",
        "diffs": diffs or [],
        "size_delta": 0,
        "suspect_binary": str(suspect),
        "trusted_binary": str(trusted),
    }


def _configure_paths(tmp_path, monkeypatch):
    quarantine_dir = tmp_path / "quarantine"
    incidents_dir = tmp_path / "incidents"
    whitelist_file = tmp_path / "whitelist.json"

    monkeypatch.setattr(responder, "QUARANTINE_DIR", str(quarantine_dir))
    monkeypatch.setattr(responder, "WHITELIST_FILE", str(whitelist_file))
    monkeypatch.setattr(reporter, "INCIDENT_DIR", str(incidents_dir))

    return quarantine_dir, incidents_dir, whitelist_file


def test_trusted_whitelists_only(tmp_path, monkeypatch):
    quarantine_dir, incidents_dir, whitelist_file = _configure_paths(tmp_path, monkeypatch)

    trusted = tmp_path / "trusted.bin"
    suspect = tmp_path / "suspect.bin"
    trusted.write_bytes(b"clean")
    suspect.write_bytes(b"clean")

    actions = responder.respond(
        _pipeline_result(suspect, trusted, verdict="TRUSTED", crack_type="clean")
    )

    assert actions == ["whitelisted"]
    assert whitelist_file.exists()

    entries = json.loads(whitelist_file.read_text(encoding="utf-8"))
    assert len(entries) == 1
    assert entries[0]["path"] == str(suspect)

    assert not quarantine_dir.exists() or not list(quarantine_dir.iterdir())
    assert not incidents_dir.exists() or not list(incidents_dir.iterdir())


def test_suspicious_quarantine_block_and_report(tmp_path, monkeypatch):
    quarantine_dir, incidents_dir, _ = _configure_paths(tmp_path, monkeypatch)

    trusted = tmp_path / "trusted.bin"
    suspect = tmp_path / "suspect.bin"
    trusted.write_bytes(b"trusted")
    suspect.write_bytes(b"suspicious")

    actions = responder.respond(
        _pipeline_result(suspect, trusted, verdict="SUSPICIOUS", crack_type="injected")
    )

    assert actions == ["quarantined", "execution_blocked", "report_generated"]
    assert not suspect.exists()

    quarantined_files = list(quarantine_dir.iterdir())
    assert len(quarantined_files) == 1

    incident_files = list(incidents_dir.glob("incident_*.json"))
    assert incident_files


def test_compromised_appended_strip_then_restore(tmp_path, monkeypatch):
    quarantine_dir, incidents_dir, _ = _configure_paths(tmp_path, monkeypatch)

    trusted = tmp_path / "trusted.bin"
    suspect = tmp_path / "suspect.bin"
    trusted.write_bytes(b"ORIGINAL")
    suspect.write_bytes(b"ORIGINALMALWARE")

    actions = responder.respond(
        _pipeline_result(suspect, trusted, verdict="COMPROMISED", crack_type="appended")
    )

    assert actions == [
        "quarantined",
        "fix_applied:appended",
        "trusted_compiler_restored",
        "incident_logged",
    ]
    assert suspect.read_bytes() == trusted.read_bytes()

    quarantined_files = list(quarantine_dir.iterdir())
    assert len(quarantined_files) == 1
    assert len(quarantined_files[0].read_bytes()) == len(trusted.read_bytes())

    incident_files = list(incidents_dir.glob("incident_*.json"))
    assert incident_files


def test_compromised_hook_nop_then_restore(tmp_path, monkeypatch):
    quarantine_dir, _, _ = _configure_paths(tmp_path, monkeypatch)

    trusted = tmp_path / "trusted.bin"
    suspect = tmp_path / "suspect.bin"
    trusted.write_bytes(b"\x01\x02\x03\x04\x05\x06\x07\x08")
    suspect.write_bytes(b"\xE9\xAA\xBB\xCC\xDD\x06\x07\x08")

    actions = responder.respond(
        _pipeline_result(
            suspect,
            trusted,
            verdict="COMPROMISED",
            crack_type="hook",
            diffs=[{"offset": "0x0"}],
        )
    )

    assert actions == [
        "quarantined",
        "fix_applied:hook",
        "trusted_compiler_restored",
        "incident_logged",
    ]
    assert suspect.read_bytes() == trusted.read_bytes()

    quarantined_files = list(quarantine_dir.iterdir())
    assert len(quarantined_files) == 1
    assert quarantined_files[0].read_bytes()[:5] == b"\x90" * 5


def test_compromised_section_uses_full_replace_action(tmp_path, monkeypatch):
    _configure_paths(tmp_path, monkeypatch)

    trusted = tmp_path / "trusted.bin"
    suspect = tmp_path / "suspect.bin"
    trusted.write_bytes(b"TRUSTED")
    suspect.write_bytes(b"BROKEN")

    actions = responder.respond(
        _pipeline_result(suspect, trusted, verdict="COMPROMISED", crack_type="section")
    )

    assert actions[1] == "fix_applied:section"
    assert suspect.read_bytes() == b"TRUSTED"
