import { motion } from "framer-motion";
import { VERDICT_STYLES } from "../data/dashboardData";

export default function VerdictBanner({ verdict }) {
    const styles = VERDICT_STYLES[verdict] || VERDICT_STYLES.TRUSTED;

    return (
        <motion.div
            initial={{ scaleX: 0, opacity: 0 }}
            animate={{ scaleX: 1, opacity: 1 }}
            transition={{ duration: 0.6, ease: "easeOut" }}
            style={{
                transformOrigin: "center",
                background: styles.bg,
                borderRadius: 8,
                padding: "20px 32px",
                textAlign: "center",
                marginBottom: 24,
                boxShadow: `0 0 40px ${styles.glow}44, inset 0 1px 0 ${styles.glow}33`,
                border: `1px solid ${styles.glow}44`,
            }}
        >
            <motion.div
                animate={{
                    textShadow: [
                        `0 0 10px ${styles.glow}`,
                        `0 0 30px ${styles.glow}`,
                        `0 0 10px ${styles.glow}`,
                    ],
                }}
                transition={{ repeat: Infinity, duration: 2 }}
                style={{
                    fontFamily: "'Share Tech Mono', monospace",
                    fontSize: 40,
                    fontWeight: 700,
                    letterSpacing: 8,
                    color: "#fff",
                }}
            >
                ⚠ {verdict}
            </motion.div>
            <div
                style={{
                    fontSize: 13,
                    color: `${styles.glow}cc`,
                    marginTop: 6,
                    fontFamily: "'Share Tech Mono', monospace",
                    letterSpacing: 2,
                }}
            >
                COMPILER INTEGRITY VALIDATION RESULT
            </div>
        </motion.div>
    );
}
