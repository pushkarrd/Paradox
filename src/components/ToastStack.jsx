import { AnimatePresence, motion } from "framer-motion";

const TONE = {
    success: { border: "#00ff9d88", glow: "#00ff9d44", text: "#00ff9d" },
    warning: { border: "#f59e0b88", glow: "#f59e0b44", text: "#f59e0b" },
    error: { border: "#ff4d4d88", glow: "#ff4d4d44", text: "#ff4d4d" },
    info: { border: "#60a5fa88", glow: "#60a5fa44", text: "#60a5fa" },
};

export default function ToastStack({ toasts, onDismiss }) {
    return (
        <div style={{ position: "fixed", right: 20, top: 20, zIndex: 10000, display: "flex", flexDirection: "column", gap: 10 }}>
            <AnimatePresence>
                {toasts.map((toast) => {
                    const color = TONE[toast.tone] || TONE.info;
                    return (
                        <motion.div
                            key={toast.id}
                            initial={{ opacity: 0, x: 24, scale: 0.96 }}
                            animate={{ opacity: 1, x: 0, scale: 1 }}
                            exit={{ opacity: 0, x: 24, scale: 0.96 }}
                            transition={{ type: "spring", stiffness: 280, damping: 24 }}
                            style={{
                                minWidth: 260,
                                maxWidth: 340,
                                background: "#0d1117f2",
                                border: `1px solid ${color.border}`,
                                borderRadius: 8,
                                padding: "10px 12px",
                                boxShadow: `0 0 18px ${color.glow}`,
                                display: "flex",
                                alignItems: "center",
                                gap: 10,
                            }}
                        >
                            <span style={{ width: 7, height: 7, borderRadius: "50%", background: color.text, flexShrink: 0 }} />
                            <span style={{ color: "#dbe5ef", fontFamily: "'Share Tech Mono', monospace", fontSize: 11, lineHeight: 1.45 }}>
                                {toast.message}
                            </span>
                            <button
                                onClick={() => onDismiss(toast.id)}
                                style={{
                                    marginLeft: "auto",
                                    background: "transparent",
                                    color: "#4a5568",
                                    border: "none",
                                    cursor: "pointer",
                                    fontSize: 12,
                                    padding: 0,
                                    lineHeight: 1,
                                }}
                            >
                                x
                            </button>
                        </motion.div>
                    );
                })}
            </AnimatePresence>
        </div>
    );
}
