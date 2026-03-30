import { motion } from "framer-motion";

export default function DiffViewer({ diffs }) {
    return (
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.4 }}>
            <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit,minmax(280px,1fr))", gap: 16 }}>
                {["suspect", "trusted"].map((side) => (
                    <div
                        key={side}
                        style={{
                            background: "#0d1117",
                            border: `1px solid ${side === "suspect" ? "#ff4d4d33" : "#00ff9d33"}`,
                            borderRadius: 8,
                            padding: "14px",
                            maxHeight: 260,
                            overflowY: "auto",
                        }}
                    >
                        <div
                            style={{
                                fontFamily: "'Share Tech Mono', monospace",
                                fontSize: 11,
                                letterSpacing: 2,
                                color: side === "suspect" ? "#ff4d4d" : "#00ff9d",
                                marginBottom: 10,
                                borderBottom: `1px solid ${side === "suspect" ? "#ff4d4d33" : "#00ff9d33"}`,
                                paddingBottom: 8,
                            }}
                        >
                            ▌ {side === "suspect" ? "SUSPECT BINARY" : "TRUSTED BINARY"}
                        </div>
                        {diffs.map((diff, index) => (
                            <motion.div
                                key={`${side}-${diff.offset}-${index}`}
                                initial={{ opacity: 0, x: side === "suspect" ? -10 : 10 }}
                                animate={{ opacity: 1, x: 0 }}
                                transition={{ delay: 0.5 + index * 0.04 }}
                                style={{
                                    fontFamily: "monospace",
                                    fontSize: 12,
                                    background: side === "suspect" ? "#ff4d4d15" : "#00ff9d15",
                                    padding: "3px 8px",
                                    marginBottom: 3,
                                    borderRadius: 4,
                                    color: side === "suspect" ? "#fca5a5" : "#86efac",
                                    borderLeft: `2px solid ${side === "suspect" ? "#ff4d4d" : "#00ff9d"}`,
                                }}
                            >
                                {diff.offset} → {side === "suspect" ? diff.suspect_byte : diff.trusted_byte}
                            </motion.div>
                        ))}
                    </div>
                ))}
            </div>
        </motion.div>
    );
}
