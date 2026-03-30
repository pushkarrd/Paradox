import { useEffect, useState } from "react";
import { motion } from "framer-motion";

export default function ScoreGauge({ score }) {
    const [displayed, setDisplayed] = useState(100);

    useEffect(() => {
        const steps = 40;
        const step = (100 - score) / steps;
        let current = 100;
        let count = 0;

        const timer = setInterval(() => {
            count += 1;
            current -= step;
            if (count >= steps) {
                setDisplayed(score);
                clearInterval(timer);
            } else {
                setDisplayed(Math.round(current));
            }
        }, 40);

        return () => clearInterval(timer);
    }, [score]);

    const color = displayed >= 90 ? "#00ff9d" : displayed >= 60 ? "#f59e0b" : "#ff4d4d";
    const pct = displayed / 100;
    const r = 80;
    const cx = 100;
    const cy = 100;
    const circ = 2 * Math.PI * r;
    const dash = circ * pct;

    return (
        <motion.div
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.3 }}
            style={{ display: "flex", flexDirection: "column", alignItems: "center" }}
        >
            <svg width={200} height={200} style={{ filter: `drop-shadow(0 0 16px ${color}55)` }}>
                <circle cx={cx} cy={cy} r={r} fill="none" stroke="#1a1a2e" strokeWidth={16} />
                <circle
                    cx={cx}
                    cy={cy}
                    r={r}
                    fill="none"
                    stroke={color}
                    strokeWidth={16}
                    strokeDasharray={`${dash} ${circ - dash}`}
                    strokeDashoffset={circ * 0.25}
                    strokeLinecap="round"
                    style={{ transition: "stroke-dasharray 0.05s linear, stroke 0.5s" }}
                />
                <text
                    x={cx}
                    y={cy - 6}
                    textAnchor="middle"
                    fill={color}
                    fontSize={36}
                    fontWeight={700}
                    fontFamily="'Share Tech Mono', monospace"
                >
                    {displayed}
                </text>
                <text
                    x={cx}
                    y={cy + 18}
                    textAnchor="middle"
                    fill="#4a5568"
                    fontSize={11}
                    fontFamily="'Share Tech Mono', monospace"
                >
                    TRUST SCORE
                </text>
            </svg>
        </motion.div>
    );
}
