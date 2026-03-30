import hashlib
import json
import os
from datetime import datetime

INCIDENT_DIR = "./incidents"


def _sha256_file(path):
    hasher = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def generate_report(pipeline_result, binary_path=None):
    """Write a JSON incident report and return the report object."""
    pr = pipeline_result
    report_binary = binary_path or pr["suspect_binary"]
    sha = None
    if os.path.exists(report_binary):
        try:
            sha = _sha256_file(report_binary)
        except OSError:
            # Quarantine may lock the file before reporting; keep report generation non-blocking.
            sha = None

    report = {
        "timestamp": datetime.now().isoformat(),
        "binary": report_binary,
        "original_binary": pr["suspect_binary"],
        "sha256": sha,
        "trust_score": pr.get("trust_score"),
        "verdict": pr["verdict"],
        "crack_type": pr["crack_type"],
        "severity": pr.get("severity"),
        "diff_count": len(pr.get("diffs", [])),
        "size_delta": pr.get("size_delta"),
        "offsets": [d.get("offset") for d in pr.get("diffs", [])[:50]],
    }

    os.makedirs(INCIDENT_DIR, exist_ok=True)
    timestamp = int(datetime.now().timestamp() * 1000)
    report_path = os.path.join(INCIDENT_DIR, f"incident_{timestamp}.json")
    with open(report_path, "w", encoding="utf-8") as handle:
        json.dump(report, handle, indent=2)

    return report
