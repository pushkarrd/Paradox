from validator import validate
from comparator import compare_binaries
from classifier import classify
from scorer import score
import os


def run_pipeline(source_path, suspect_compiler, trusted_compiler):

    # Step 1: Validate (compile)
    paths = validate(source_path, suspect_compiler, trusted_compiler)

    # If compilation failed
    if paths["errors"]["suspect"]:
        return {"error": paths["errors"]["suspect"]}

    if paths["errors"]["trusted"]:
        return {"error": paths["errors"]["trusted"]}

    # Step 2: Compare binaries
    diffs, size_delta = compare_binaries(
        paths["suspect"], paths["trusted"]
    )

    # Step 3: Classify
    crack_type, severity = classify(
        paths["suspect"], paths["trusted"], diffs, size_delta
    )

    # Step 4: Get total bytes
    total_bytes = os.path.getsize(paths["suspect"])

    # Step 5: Score
    trust_score, verdict = score(
        diffs, size_delta, total_bytes, severity
    )

    # Final Output (API contract)
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