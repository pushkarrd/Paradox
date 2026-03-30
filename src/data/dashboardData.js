export const MOCK_RESULT = {
    verdict: "COMPROMISED",
    trust_score: 34,
    crack_type: "injected",
    severity: "CRITICAL",
    diffs: Array.from({ length: 12 }, (_, i) => ({
        offset: `0x${(0x4005a0 + i * 4).toString(16).toUpperCase()}`,
        suspect_byte: `0x${Math.floor(Math.random() * 255)
            .toString(16)
            .padStart(2, "0")
            .toUpperCase()}`,
        trusted_byte: `0x${Math.floor(Math.random() * 255)
            .toString(16)
            .padStart(2, "0")
            .toUpperCase()}`,
    })),
    actions: [
        "quarantined",
        "execution_blocked",
        "fix_applied:injected",
        "trusted_compiler_restored",
        "report_generated",
        "incident_logged",
    ],
    report: {
        timestamp: new Date().toISOString(),
        verdict: "COMPROMISED",
        trust_score: 34,
        crack_type: "injected",
        severity: "CRITICAL",
        diffs_count: 12,
        actions_taken: ["quarantined", "execution_blocked", "fix_applied:injected"],
    },
};

export const PAST_INCIDENTS = [
    { id: "INC-001", verdict: "COMPROMISED", score: 21, type: "hook", time: "2h ago" },
    { id: "INC-002", verdict: "SUSPICIOUS", score: 67, type: "syscall", time: "5h ago" },
    { id: "INC-003", verdict: "TRUSTED", score: 98, type: "none", time: "1d ago" },
    { id: "INC-004", verdict: "COMPROMISED", score: 14, type: "section", time: "2d ago" },
];

export const ACTION_META = {
    whitelisted: { icon: "✓", color: "#00ff9d", label: "Binary approved and whitelisted" },
    quarantined: { icon: "⛔", color: "#ff4d4d", label: "Suspect binary moved to quarantine" },
    execution_blocked: {
        icon: "🚫",
        color: "#ff4d4d",
        label: "Execute permissions stripped from binary",
    },
    "fix_applied:appended": {
        icon: "🔧",
        color: "#f59e0b",
        label: "Injected bytes stripped from end of binary",
    },
    "fix_applied:injected": {
        icon: "🔧",
        color: "#f59e0b",
        label: "Patched injected bytes at differing offsets",
    },
    "fix_applied:hook": {
        icon: "🔧",
        color: "#f59e0b",
        label: "Function hook removed - NOP-slid over JMP",
    },
    "fix_applied:syscall": {
        icon: "🔧",
        color: "#f59e0b",
        label: "Injected syscall instruction erased",
    },
    "fix_applied:section": {
        icon: "🔧",
        color: "#ff4d4d",
        label: "Injected ELF section removed - full replace",
    },
    trusted_compiler_restored: { icon: "↻", color: "#00ff9d", label: "Trusted compiler binary restored" },
    report_generated: { icon: "📄", color: "#60a5fa", label: "Incident report generated" },
    incident_logged: { icon: "📄", color: "#60a5fa", label: "Incident added to audit log" },
};

export const VERDICT_STYLES = {
    COMPROMISED: { bg: "linear-gradient(135deg,#7f1d1d,#991b1b)", glow: "#ff4d4d", accent: "#ff4d4d" },
    SUSPICIOUS: { bg: "linear-gradient(135deg,#78350f,#92400e)", glow: "#f59e0b", accent: "#f59e0b" },
    TRUSTED: { bg: "linear-gradient(135deg,#14532d,#166534)", glow: "#00ff9d", accent: "#00ff9d" },
};
