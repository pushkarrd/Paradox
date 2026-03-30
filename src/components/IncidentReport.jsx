import { useState } from "react";
import { AnimatePresence, motion } from "framer-motion";

export default function IncidentReport({ report }) {
    const [expanded, setExpanded] = useState(false);
    const json = JSON.stringify(report, null, 2);

    const handleDownload = () => {
        const blob = new Blob([json], { type: "application/json" });
        const href = URL.createObjectURL(blob);
        const anchor = Object.assign(document.createElement("a"), {
            href,
            download: "incident_report.json",
        });
        anchor.click();
        setTimeout(() => URL.revokeObjectURL(href), 1000);
    };

    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.6 }}
            style={{ background: "#0d1117", border: "1px solid #60a5fa33", borderRadius: 8, overflow: "hidden" }}
        >
            <div
                onClick={() => setExpanded((value) => !value)}
                style={{
                    padding: "12px 18px",
                    cursor: "pointer",
                    display: "flex",
                    justifyContent: "space-between",
                    alignItems: "center",
                    borderBottom: expanded ? "1px solid #60a5fa22" : "none",
                }}
            >
                <span
                    style={{
                        fontFamily: "'Share Tech Mono', monospace",
                        fontSize: 13,
                        color: "#60a5fa",
                        letterSpacing: 1,
                    }}
                >
                    📄 INCIDENT REPORT
                </span>
                <span style={{ color: "#4a5568", fontSize: 18 }}>{expanded ? "▲" : "▼"}</span>
            </div>
            <AnimatePresence>
                {expanded && (
                    <motion.div initial={{ height: 0 }} animate={{ height: "auto" }} exit={{ height: 0 }} style={{ overflow: "hidden" }}>
                        <pre
                            style={{
                                padding: "16px 18px",
                                fontFamily: "monospace",
                                fontSize: 12,
                                color: "#86efac",
                                overflowX: "auto",
                                margin: 0,
                                background: "#060910",
                            }}
                        >
                            {json}
                        </pre>
                        <div style={{ padding: "12px 18px", borderTop: "1px solid #60a5fa22" }}>
                            <button
                                onClick={handleDownload}
                                style={{
                                    background: "linear-gradient(135deg,#1e3a5f,#1d4ed8)",
                                    border: "1px solid #60a5fa",
                                    color: "#60a5fa",
                                    padding: "8px 20px",
                                    borderRadius: 6,
                                    cursor: "pointer",
                                    fontFamily: "'Share Tech Mono', monospace",
                                    fontSize: 12,
                                    letterSpacing: 1,
                                }}
                            >
                                ↓ DOWNLOAD JSON
                            </button>
                        </div>
                    </motion.div>
                )}
            </AnimatePresence>
        </motion.div>
    );
}
