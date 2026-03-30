import { motion } from "framer-motion";

export default function IncidentHistory({ incidents }) {
    const verdictColor = { COMPROMISED: "#ff4d4d", SUSPICIOUS: "#f59e0b", TRUSTED: "#00ff9d" };

    return (
        <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.2 }}
            style={{ background: "#0d1117", border: "1px solid #1e293b", borderRadius: 8, padding: "16px" }}
        >
            <div
                style={{
                    fontFamily: "'Share Tech Mono', monospace",
                    fontSize: 10,
                    letterSpacing: 3,
                    color: "#4a5568",
                    marginBottom: 14,
                }}
            >
                PAST INCIDENTS
            </div>
            {incidents.map((incident, index) => (
                <motion.div
                    key={incident.id}
                    initial={{ opacity: 0, x: 20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: index * 0.08 }}
                    style={{
                        display: "flex",
                        alignItems: "center",
                        gap: 10,
                        padding: "8px 0",
                        borderBottom: index < incidents.length - 1 ? "1px solid #1e293b" : "none",
                    }}
                >
                    <div
                        style={{
                            width: 6,
                            height: 6,
                            borderRadius: "50%",
                            background: verdictColor[incident.verdict],
                        }}
                    />
                    <span style={{ fontFamily: "monospace", fontSize: 11, color: "#4a5568", flex: 1 }}>{incident.id}</span>
                    <span
                        style={{
                            fontFamily: "'Share Tech Mono', monospace",
                            fontSize: 10,
                            color: verdictColor[incident.verdict],
                        }}
                    >
                        {incident.verdict}
                    </span>
                    <span style={{ fontFamily: "monospace", fontSize: 11, color: "#4a5568" }}>{incident.time}</span>
                </motion.div>
            ))}
        </motion.div>
    );
}
