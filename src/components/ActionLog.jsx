import { useEffect, useState } from "react";
import { AnimatePresence, motion } from "framer-motion";
import { ACTION_META } from "../data/dashboardData";

export default function ActionLog({ actions }) {
    const [visible, setVisible] = useState([]);

    useEffect(() => {
        setVisible([]);
        const timers = actions.map((action, index) =>
            setTimeout(() => {
                setVisible((current) => [...current, action]);
            }, index * 400 + 600),
        );

        return () => {
            timers.forEach((timer) => clearTimeout(timer));
        };
    }, [actions]);

    return (
        <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
            <AnimatePresence>
                {visible.map((action, index) => {
                    const meta = ACTION_META[action] || { icon: "•", color: "#60a5fa", label: action };
                    return (
                        <motion.div
                            key={`${action}-${index}`}
                            initial={{ opacity: 0, x: -30, height: 0 }}
                            animate={{ opacity: 1, x: 0, height: "auto" }}
                            transition={{ type: "spring", stiffness: 200, damping: 20 }}
                            style={{
                                background: "#0d1117",
                                border: `1px solid ${meta.color}33`,
                                borderRadius: 6,
                                padding: "10px 14px",
                                display: "flex",
                                alignItems: "center",
                                gap: 12,
                            }}
                        >
                            <span style={{ fontSize: 18 }}>{meta.icon}</span>
                            <span style={{ fontFamily: "'Share Tech Mono', monospace", fontSize: 13, color: meta.color }}>
                                {meta.label}
                            </span>
                            <span style={{ marginLeft: "auto", fontFamily: "monospace", fontSize: 10, color: "#4a5568" }}>
                                {new Date().toLocaleTimeString()}
                            </span>
                        </motion.div>
                    );
                })}
            </AnimatePresence>
        </div>
    );
}
