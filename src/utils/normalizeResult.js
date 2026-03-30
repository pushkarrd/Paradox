import { MOCK_RESULT } from "../data/dashboardData";

export function normalizeResult(raw) {
    if (!raw || typeof raw !== "object") {
        return MOCK_RESULT;
    }

    return {
        verdict: raw.verdict || "SUSPICIOUS",
        trust_score: Number.isFinite(raw.trust_score) ? raw.trust_score : 50,
        crack_type: raw.crack_type || "unknown",
        severity: raw.severity || "HIGH",
        diffs: Array.isArray(raw.diffs) ? raw.diffs : [],
        actions: Array.isArray(raw.actions) ? raw.actions : [],
        report: raw.report || {
            timestamp: new Date().toISOString(),
            verdict: raw.verdict || "SUSPICIOUS",
            trust_score: Number.isFinite(raw.trust_score) ? raw.trust_score : 50,
            crack_type: raw.crack_type || "unknown",
            severity: raw.severity || "HIGH",
            diffs_count: Array.isArray(raw.diffs) ? raw.diffs.length : 0,
            actions_taken: Array.isArray(raw.actions) ? raw.actions : [],
        },
    };
}
