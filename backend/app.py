from flask import Flask, jsonify, request
from flask_cors import CORS
from werkzeug.utils import secure_filename
import json
import os
import time

from pipeline import run_pipeline
from responder import respond
from reporter import generate_report

APP_START_TIME = time.time()

app = Flask(__name__)
CORS(app, origins=["http://localhost:5173"])

app.config.setdefault("INCIDENTS_DIR", os.path.join(".", "incidents"))
app.config.setdefault("WHITELIST_PATH", os.path.join(".", "whitelist.json"))
app.config.setdefault("UPLOAD_DIR", os.path.join(".", "uploads"))


def json_error(message, status_code):
    return jsonify({"error": message}), status_code


@app.route("/api/validate", methods=["POST"])
def validate():
    try:
        data = request.get_json(silent=True) or {}
        source = data.get("source_path")
        suspect = data.get("suspect_compiler")
        trusted = data.get("trusted_compiler")

        if not all([source, suspect, trusted]):
            return json_error("Missing required fields", 400)

        pr = run_pipeline(source, suspect, trusted)
        if not isinstance(pr, dict):
            return json_error("Pipeline returned invalid response", 500)
        if pr.get("error"):
            return json_error(pr.get("error"), 500)

        actions = respond(pr)
        report = generate_report(pr)
        diffs = pr.get("diffs") or []
        if not isinstance(diffs, list):
            diffs = []

        return jsonify(
            {
                "score": pr.get("trust_score"),
                "verdict": pr.get("verdict"),
                "crack_type": pr.get("crack_type"),
                "severity": pr.get("severity"),
                "diffs": diffs[:50],
                "actions": actions,
                "report": report,
                "error": None,
            }
        )
    except Exception as exc:
        return json_error(str(exc), 500)


@app.route("/api/incidents", methods=["GET"])
def list_incidents():
    try:
        inc_dir = app.config["INCIDENTS_DIR"]
        if not os.path.exists(inc_dir):
            return jsonify([])

        files = sorted(os.listdir(inc_dir), reverse=True)
        reports = []
        for filename in files[:20]:
            path = os.path.join(inc_dir, filename)
            if not os.path.isfile(path):
                continue
            try:
                with open(path, "r", encoding="utf-8") as handle:
                    reports.append(json.load(handle))
            except Exception:
                continue
        return jsonify(reports)
    except Exception as exc:
        return json_error(str(exc), 500)


@app.route("/api/whitelist", methods=["GET"])
def get_whitelist():
    try:
        path = app.config["WHITELIST_PATH"]
        if not os.path.exists(path):
            return jsonify([])
        with open(path, "r", encoding="utf-8") as handle:
            return jsonify(json.load(handle))
    except Exception as exc:
        return json_error(str(exc), 500)


@app.route("/api/status", methods=["GET"])
def status():
    uptime = int(time.time() - APP_START_TIME)
    return jsonify({"status": "ok", "version": "1.0.0", "uptime": uptime})


@app.route("/api/upload", methods=["POST"])
def upload():
    try:
        upload_file = request.files.get("source")
        if not upload_file:
            return json_error("No file", 400)

        filename = secure_filename(upload_file.filename)
        if not filename:
            return json_error("Invalid filename", 400)

        upload_dir = app.config["UPLOAD_DIR"]
        os.makedirs(upload_dir, exist_ok=True)
        saved_path = os.path.join(upload_dir, filename)
        upload_file.save(saved_path)

        return jsonify({"saved_path": saved_path, "filename": filename})
    except Exception as exc:
        return json_error(str(exc), 500)


@app.route("/api/report/<incident_id>", methods=["GET"])
def report(incident_id):
    try:
        inc_dir = app.config["INCIDENTS_DIR"]
        candidates = [incident_id, f"{incident_id}.json"]

        for name in candidates:
            path = os.path.join(inc_dir, name)
            if os.path.isfile(path):
                with open(path, "r", encoding="utf-8") as handle:
                    return jsonify(json.load(handle))

        return json_error("Incident not found", 404)
    except Exception as exc:
        return json_error(str(exc), 500)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
