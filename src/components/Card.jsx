import { motion } from "framer-motion";

export default function Card({ title, children, delay = 0, accent = "#00ff9d" }) {
    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay }}
            style={{
                background: "#0d1117",
                border: "1px solid #1e293b",
                borderRadius: 10,
                padding: "20px",
                marginBottom: 20,
                boxShadow: "0 0 0 1px #00000088",
            }}
        >
            <div
                style={{
                    fontFamily: "'Share Tech Mono', monospace",
                    fontSize: 10,
                    letterSpacing: 3,
                    color: accent,
                    marginBottom: 16,
                    display: "flex",
                    alignItems: "center",
                    gap: 8,
                }}
            >
                <span style={{ display: "inline-block", width: 16, height: 1, background: accent }} />
                {title}
                <span style={{ flex: 1, height: 1, background: `${accent}22` }} />
            </div>
            {children}
        </motion.div>
    );
}
