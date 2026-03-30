import { useEffect, useState } from "react";

export default function GlitchText({ text, size = 14, color = "#00ff9d" }) {
    const [glitching, setGlitching] = useState(false);

    useEffect(() => {
        const localTimers = [];
        const tick = setInterval(() => {
            setGlitching(true);
            localTimers.push(setTimeout(() => setGlitching(false), 120));
        }, 3000 + Math.random() * 2000);

        return () => {
            clearInterval(tick);
            localTimers.forEach((timer) => clearTimeout(timer));
        };
    }, []);

    return (
        <span
            style={{
                position: "relative",
                fontSize: size,
                fontFamily: "'Share Tech Mono', monospace",
                color,
            }}
        >
            {text}
            {glitching && (
                <span
                    style={{
                        position: "absolute",
                        left: 2,
                        top: 0,
                        color: "#ff4d4d",
                        clipPath: "polygon(0 30%, 100% 30%, 100% 50%, 0 50%)",
                        opacity: 0.8,
                    }}
                >
                    {text}
                </span>
            )}
        </span>
    );
}
