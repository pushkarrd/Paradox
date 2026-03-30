from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import sys
from datetime import datetime, timezone

from run_pipeline import run_pipeline

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
CORS(app)


def _resolve_path(value):
    if not isinstance(value, str):
        return value

    trimmed = value.strip()
    if not trimmed:
        return trimmed

    if os.path.isabs(trimmed):
        return trimmed

    return os.path.normpath(os.path.join(BASE_DIR, trimmed))


def _normalize_compiler(value, default):
    raw = value if value else default

    if isinstance(raw, list):
        normalized = []
        for part in raw:
            normalized.append(_resolve_path(part) if isinstance(part, str) else part)
        return normalized

    if isinstance(raw, str):
        resolved = _resolve_path(raw)
        if isinstance(resolved, str) and resolved.lower().endswith(".py"):
            return [sys.executable, resolved]
        return resolved

    return raw


def _derive_actions(verdict, crack_type):
    actions = []

    if verdict == "TRUSTED":
        actions.append("whitelisted")
    else:
        actions.extend(["quarantined", "execution_blocked"])
        if crack_type and crack_type not in {"clean", "timestamp", "none"}:
            actions.append(f"fix_applied:{crack_type}")
        actions.append("trusted_compiler_restored")

    actions.extend(["report_generated", "incident_logged"])
    return actions


def _shape_frontend_payload(engine_result):
    verdict = str(engine_result.get("verdict", "SUSPICIOUS")).upper()
    crack_type = str(engine_result.get("crack_type", "unknown")).lower()
    severity = str(engine_result.get("severity", "none")).upper()
    trust_score = int(engine_result.get("trust_score", 0))
    diffs = engine_result.get("diffs") or []
    actions = _derive_actions(verdict, crack_type)

    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "verdict": verdict,
        "trust_score": trust_score,
        "crack_type": crack_type,
        "severity": severity,
        "diffs_count": len(diffs),
        "actions_taken": actions,
    }

    return {
        "verdict": verdict,
        "trust_score": trust_score,
        "crack_type": crack_type,
        "severity": severity,
        "diffs": diffs,
        "actions": actions,
        "report": report,
        "meta": {
            "suspect_binary": engine_result.get("suspect_binary"),
            "trusted_binary": engine_result.get("trusted_binary"),
            "size_delta": engine_result.get("size_delta"),
            "total_bytes": engine_result.get("total_bytes"),
        },
    }


@app.get("/health")
def health():
    return jsonify({"ok": True})


@app.post("/api/validate")
def validate():
    payload = request.get_json(silent=True) or {}

    source_path = _resolve_path(payload.get("source", "samples/clean.c"))
    suspect_compiler = _normalize_compiler(payload.get("suspect"), "samples/fake_compiler.py")
    trusted_compiler = _normalize_compiler(payload.get("trusted"), "gcc")

    try:
        result = run_pipeline(source_path, suspect_compiler, trusted_compiler)
    except Exception as exc:
        return jsonify({"error": f"Pipeline execution failed: {exc}"}), 500

    if result.get("error"):
        return jsonify(result), 400

    return jsonify(_shape_frontend_payload(result))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
