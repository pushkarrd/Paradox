export function normalizeResult(raw) {
    if (!raw || typeof raw !== "object") {
        return null;
    }

    const trustScoreValue = Number.isFinite(raw.trust_score)
        ? raw.trust_score
        : Number.isFinite(raw.score)
            ? raw.score
            : 50;

    return {
        verdict: raw.verdict || "SUSPICIOUS",
        trust_score: trustScoreValue,
        crack_type: raw.crack_type || "unknown",
        severity: raw.severity || "HIGH",
        diffs: Array.isArray(raw.diffs) ? raw.diffs : [],
        actions: Array.isArray(raw.actions) ? raw.actions : [],
        report: raw.report || {
            timestamp: new Date().toISOString(),
            verdict: raw.verdict || "SUSPICIOUS",
            trust_score: trustScoreValue,
            crack_type: raw.crack_type || "unknown",
            severity: raw.severity || "HIGH",
            diffs_count: Array.isArray(raw.diffs) ? raw.diffs.length : 0,
            actions_taken: Array.isArray(raw.actions) ? raw.actions : [],
        },
    };
}
