import { motion } from "framer-motion";

export default function CrackTypeBadge({ crackType, severity }) {
    const severityColors = {
        CRITICAL: "#ff4d4d",
        HIGH: "#f59e0b",
        MEDIUM: "#facc15",
        LOW: "#00ff9d",
    };
    const sevColor = severityColors[severity] || "#60a5fa";

    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            style={{ display: "flex", gap: 12, alignItems: "center", flexWrap: "wrap" }}
        >
            <div
                style={{
                    background: "#0d1117",
                    border: "1px solid #30363d",
                    borderRadius: 6,
                    padding: "6px 16px",
                    fontFamily: "'Share Tech Mono', monospace",
                    fontSize: 13,
                    color: "#e6edf3",
                    letterSpacing: 1,
                }}
            >
                INJECTION TYPE: <span style={{ color: "#60a5fa" }}>{crackType?.toUpperCase() || "UNKNOWN"}</span>
            </div>
            <div
                style={{
                    background: `${sevColor}22`,
                    border: `1px solid ${sevColor}`,
                    borderRadius: 20,
                    padding: "4px 14px",
                    fontFamily: "'Share Tech Mono', monospace",
                    fontSize: 12,
                    fontWeight: 700,
                    color: sevColor,
                    letterSpacing: 2,
                }}
            >
                {severity}
            </div>
        </motion.div>
    );
}
