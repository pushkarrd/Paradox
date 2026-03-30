import { motion } from "framer-motion";
import GlitchText from "./GlitchText";

export default function AppHeader({ phase, onReset }) {
    return (
        <motion.header
            initial={{ y: -60, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            style={{
                padding: "20px 0",
                marginBottom: 8,
                borderBottom: "1px solid #1e293b",
                display: "flex",
                alignItems: "center",
                justifyContent: "space-between",
                gap: 18,
                flexWrap: "wrap",
            }}
        >
            <div style={{ display: "flex", alignItems: "center", gap: 14 }}>
                <motion.div
                    animate={{ rotate: [0, 360] }}
                    transition={{ repeat: Infinity, duration: 12, ease: "linear" }}
                    style={{
                        width: 32,
                        height: 32,
                        border: "2px solid #00ff9d",
                        borderRadius: "50%",
                        display: "flex",
                        alignItems: "center",
                        justifyContent: "center",
                        color: "#00ff9d",
                        fontSize: 16,
                    }}
                >
                    ⬡
                </motion.div>
                <div>
                    <GlitchText text="COMPILER VALIDATION TOOL" size={15} color="#e6edf3" />
                    <div
                        style={{
                            fontFamily: "'Share Tech Mono', monospace",
                            fontSize: 10,
                            color: "#4a5568",
                            letterSpacing: 2,
                            marginTop: 2,
                        }}
                    >
                        TRUST SCORE ENGINE v2.4.1
                    </div>
                </div>
            </div>

            <div style={{ display: "flex", gap: 20, alignItems: "center" }}>
                <motion.div
                    animate={{ opacity: [0.4, 1, 0.4] }}
                    transition={{ repeat: Infinity, duration: 2 }}
                    style={{
                        display: "flex",
                        alignItems: "center",
                        gap: 6,
                        fontFamily: "'Share Tech Mono', monospace",
                        fontSize: 11,
                        color: "#00ff9d",
                    }}
                >
                    <span
                        style={{
                            width: 6,
                            height: 6,
                            borderRadius: "50%",
                            background: "#00ff9d",
                            display: "inline-block",
                        }}
                    />
                    SYSTEM ONLINE
                </motion.div>

                {phase !== "input" && (
                    <motion.button
                        whileHover={{ scale: 1.05 }}
                        whileTap={{ scale: 0.95 }}
                        onClick={onReset}
                        style={{
                            background: "transparent",
                            border: "1px solid #30363d",
                            borderRadius: 6,
                            color: "#4a5568",
                            padding: "6px 14px",
                            cursor: "pointer",
                            fontFamily: "'Share Tech Mono', monospace",
                            fontSize: 11,
                            letterSpacing: 1,
                        }}
                    >
                        ← NEW SCAN
                    </motion.button>
                )}
            </div>
        </motion.header>
    );
}
