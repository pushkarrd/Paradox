import os

from classifier import classify
from comparator import compare_binaries
from scorer import score
from validator import validate


def run_pipeline(source_path, suspect_compiler, trusted_compiler):
    paths = validate(source_path, suspect_compiler, trusted_compiler)

    if paths["errors"]["suspect"] and not paths["suspect"]:
        return {"error": paths["errors"]["suspect"]}

    if paths["errors"]["trusted"] and not paths["trusted"]:
        return {"error": paths["errors"]["trusted"]}

    if not paths["suspect"] or not paths["trusted"]:
        return {"error": "Compilation failed", "details": paths["errors"]}

    diffs, size_delta = compare_binaries(paths["suspect"], paths["trusted"])
    crack_type, severity = classify(paths["suspect"], paths["trusted"], diffs, size_delta)
    total_bytes = os.path.getsize(paths["suspect"])
    trust_score, verdict = score(diffs, size_delta, total_bytes, severity)

    return {
        "suspect_binary": paths["suspect"],
        "trusted_binary": paths["trusted"],
        "diffs": diffs,
        "size_delta": size_delta,
        "crack_type": crack_type,
        "severity": severity,
        "trust_score": trust_score,
        "verdict": verdict,
        "total_bytes": total_bytes,
        "error": None,
    }
