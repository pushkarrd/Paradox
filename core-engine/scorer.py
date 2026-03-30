SEVERITY_PENALTY = {
    "none": 0.0,
    "medium": 0.15,
    "high": 0.30,
    "critical": 0.50,
}


def score(diffs, size_delta, total_bytes, severity):

    # Perfect case
    if not diffs and size_delta == 0:
        return 100, "TRUSTED"

    # Ratio of differences
    diff_ratio = len(diffs) / max(total_bytes, 1)

    # Size penalty (max capped)
    size_penalty = min(abs(size_delta) / 500, 0.3)

    # Severity penalty
    severity_penalty = SEVERITY_PENALTY.get(severity, 0)

    # Final score calculation
    raw_score = max(0, 1.0 - diff_ratio - size_penalty - severity_penalty)

    trust_score = int(raw_score * 100)

    # Verdict
    if trust_score >= 90:
        verdict = "TRUSTED"
    elif trust_score >= 60:
        verdict = "SUSPICIOUS"
    else:
        verdict = "COMPROMISED"

    return trust_score, verdict