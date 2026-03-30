import { useEffect, useState } from "react";
import { motion } from "framer-motion";

export default function Pipeline({ onDone }) {
    const steps = ["COMPILING", "COMPARING", "CLASSIFYING", "SCORING"];
    const [active, setActive] = useState(0);

    useEffect(() => {
        const timers = [];

        steps.forEach((_, index) => {
            const timer = setTimeout(() => {
                setActive(index + 1);
                if (index === steps.length - 1) {
                    timers.push(setTimeout(onDone, 500));
                }
            }, (index + 1) * 600);
            timers.push(timer);
        });

        return () => {
            timers.forEach((timer) => clearTimeout(timer));
        };
    }, [onDone]);

    return (
        <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            style={{
                maxWidth: 560,
                margin: "80px auto",
                padding: "48px",
                background: "#0d1117",
                border: "1px solid #30363d",
                borderRadius: 12,
            }}
        >
            <div
                style={{
                    fontFamily: "'Share Tech Mono', monospace",
                    fontSize: 13,
                    color: "#4a5568",
                    letterSpacing: 2,
                    marginBottom: 36,
                    textAlign: "center",
                }}
            >
                ANALYSIS PIPELINE RUNNING
            </div>
            <div style={{ display: "flex", flexDirection: "column", gap: 20 }}>
                {steps.map((step, index) => {
                    const done = active > index;
                    const current = active === index;

                    return (
                        <motion.div key={step} style={{ display: "flex", alignItems: "center", gap: 16 }}>
                            <motion.div
                                animate={done ? { scale: [1, 1.3, 1] } : { scale: 1 }}
                                transition={{ duration: 0.35 }}
                                style={{
                                    width: 28,
                                    height: 28,
                                    borderRadius: "50%",
                                    display: "flex",
                                    alignItems: "center",
                                    justifyContent: "center",
                                    background: done ? "#00ff9d22" : "#0d1117",
                                    border: `2px solid ${done ? "#00ff9d" : current ? "#60a5fa" : "#1e293b"}`,
                                    color: done ? "#00ff9d" : current ? "#60a5fa" : "#1e293b",
                                    fontSize: 14,
                                    fontWeight: 700,
                                }}
                            >
                                {done ? "✓" : index + 1}
                            </motion.div>
                            <div style={{ flex: 1 }}>
                                <div
                                    style={{
                                        fontFamily: "'Share Tech Mono', monospace",
                                        fontSize: 12,
                                        letterSpacing: 2,
                                        color: done ? "#00ff9d" : current ? "#60a5fa" : "#1e293b",
                                    }}
                                >
                                    {step}
                                </div>
                                {(done || current) && (
                                    <div style={{ height: 2, background: "#1e293b", borderRadius: 2, marginTop: 6 }}>
                                        <motion.div
                                            initial={{ width: 0 }}
                                            animate={{ width: "100%" }}
                                            transition={{ duration: 0.45 }}
                                            style={{
                                                height: "100%",
                                                background: done ? "#00ff9d" : "#60a5fa",
                                                borderRadius: 2,
                                            }}
                                        />
                                    </div>
                                )}
                            </div>
                            {current && (
                                <motion.div
                                    animate={{ rotate: 360 }}
                                    transition={{ repeat: Infinity, duration: 0.8, ease: "linear" }}
                                    style={{ color: "#60a5fa", fontSize: 16 }}
                                >
                                    ↻
                                </motion.div>
                            )}
                        </motion.div>
                    );
                })}
            </div>
        </motion.div>
    );
}
