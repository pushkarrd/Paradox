export default function Scanlines() {
    return (
        <div
            style={{
                position: "fixed",
                inset: 0,
                pointerEvents: "none",
                zIndex: 9999,
                backgroundImage:
                    "repeating-linear-gradient(0deg,transparent,transparent 2px,rgba(0,255,157,0.015) 2px,rgba(0,255,157,0.015) 4px)",
            }}
        />
    );
}
