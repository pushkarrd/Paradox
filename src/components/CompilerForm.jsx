import { useState } from "react";
import { motion } from "framer-motion";

export default function CompilerForm({ onSubmit }) {
    const [source, setSource] = useState("samples/clean.c");
    const [suspect, setSuspect] = useState("backend/fake_compiler.py");
    const [trusted, setTrusted] = useState("gcc");

    const fields = [
        { label: "SOURCE FILE PATH", value: source, set: setSource, icon: "📁" },
        { label: "SUSPECT COMPILER", value: suspect, set: setSuspect, icon: "⚠" },
        { label: "TRUSTED COMPILER", value: trusted, set: setTrusted, icon: "✓" },
    ];

    return (
        <motion.div
            initial={{ opacity: 0, y: 40 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.7 }}
            style={{ maxWidth: 580, margin: "0 auto", padding: "48px 0" }}
        >
            <motion.div style={{ textAlign: "center", marginBottom: 48 }}>
                <motion.div
                    animate={{ opacity: [0.5, 1, 0.5] }}
                    transition={{ repeat: Infinity, duration: 3 }}
                    style={{
                        fontFamily: "'Share Tech Mono', monospace",
                        fontSize: 11,
                        letterSpacing: 4,
                        color: "#00ff9d",
                        marginBottom: 16,
                    }}
                >
                    ◈ COMPILER INTEGRITY VALIDATOR ◈
                </motion.div>
                <div
                    style={{
                        fontFamily: "'Share Tech Mono', monospace",
                        fontSize: 28,
                        color: "#e6edf3",
                        letterSpacing: 2,
                        marginBottom: 12,
                    }}
                >
                    VALIDATE COMPILER
                </div>
                <div
                    style={{
                        fontFamily: "'Share Tech Mono', monospace",
                        fontSize: 12,
                        color: "#4a5568",
                        lineHeight: 1.8,
                    }}
                >
                    We compile your source with both compilers
                    <br />
                    and compare the output binaries for injection signatures.
                </div>
            </motion.div>

            <div style={{ display: "flex", flexDirection: "column", gap: 20, marginBottom: 36 }}>
                {fields.map((field, index) => (
                    <motion.div
                        key={field.label}
                        initial={{ opacity: 0, x: -20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: index * 0.12 }}
                    >
                        <div
                            style={{
                                fontFamily: "'Share Tech Mono', monospace",
                                fontSize: 10,
                                color: "#4a5568",
                                letterSpacing: 2,
                                marginBottom: 8,
                            }}
                        >
                            {field.icon} {field.label}
                        </div>
                        <input
                            value={field.value}
                            onChange={(event) => field.set(event.target.value)}
                            style={{
                                width: "100%",
                                background: "#0d1117",
                                border: "1px solid #30363d",
                                borderRadius: 6,
                                padding: "12px 16px",
                                color: "#e6edf3",
                                fontFamily: "'Share Tech Mono', monospace",
                                fontSize: 13,
                                outline: "none",
                                boxSizing: "border-box",
                                transition: "border-color 0.2s, box-shadow 0.2s",
                            }}
                            onFocus={(event) => {
                                event.target.style.borderColor = "#00ff9d";
                                event.target.style.boxShadow = "0 0 18px #00ff9d33";
                            }}
                            onBlur={(event) => {
                                event.target.style.borderColor = "#30363d";
                                event.target.style.boxShadow = "none";
                            }}
                        />
                    </motion.div>
                ))}
            </div>

            <motion.button
                whileHover={{
                    scale: 1.02,
                    boxShadow: ["0 0 18px #00ff9d44", "0 0 36px #00ff9d88", "0 0 18px #00ff9d44"],
                    transition: { duration: 0.9, repeat: Infinity, ease: "easeInOut" },
                }}
                whileTap={{ scale: 0.97 }}
                onClick={() => onSubmit({ source, suspect, trusted })}
                style={{
                    width: "100%",
                    padding: "16px",
                    background: "linear-gradient(135deg,#064e3b,#065f46)",
                    border: "1px solid #00ff9d55",
                    borderRadius: 8,
                    color: "#00ff9d",
                    fontFamily: "'Share Tech Mono', monospace",
                    fontSize: 16,
                    letterSpacing: 4,
                    cursor: "pointer",
                    boxShadow: "0 0 20px #00ff9d22",
                }}
            >
                ▶ RUN VALIDATION
            </motion.button>
        </motion.div>
    );
}
