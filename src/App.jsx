import { useEffect, useRef, useState } from "react";
import { AnimatePresence, motion } from "framer-motion";
import ActionLog from "./components/ActionLog";
import AppHeader from "./components/AppHeader";
import Card from "./components/Card";
import CompilerForm from "./components/CompilerForm";
import CrackTypeBadge from "./components/CrackTypeBadge";
import DiffViewer from "./components/DiffViewer";
import IncidentHistory from "./components/IncidentHistory";
import IncidentReport from "./components/IncidentReport";
import Pipeline from "./components/Pipeline";
import Scanlines from "./components/Scanlines";
import ScoreGauge from "./components/ScoreGauge";
import ToastStack from "./components/ToastStack";
import VerdictBanner from "./components/VerdictBanner";
import { MOCK_RESULT, PAST_INCIDENTS } from "./data/dashboardData";
import { normalizeResult } from "./utils/normalizeResult";

export default function App() {
  const [phase, setPhase] = useState("input");
  const [result, setResult] = useState(null);
  const [pipelineFinished, setPipelineFinished] = useState(false);
  const [isNarrow, setIsNarrow] = useState(() => window.innerWidth < 1080);
  const [toasts, setToasts] = useState([]);
  const toastTimers = useRef(new Map());

  const dismissToast = (id) => {
    setToasts((current) => current.filter((toast) => toast.id !== id));
    const timer = toastTimers.current.get(id);
    if (timer) {
      clearTimeout(timer);
      toastTimers.current.delete(id);
    }
  };

  const pushToast = (message, tone = "info", timeout = 3200) => {
    const id = `${Date.now()}-${Math.random().toString(16).slice(2)}`;
    setToasts((current) => [...current, { id, message, tone }]);
    const timer = setTimeout(() => dismissToast(id), timeout);
    toastTimers.current.set(id, timer);
  };

  useEffect(() => {
    const onResize = () => setIsNarrow(window.innerWidth < 1080);
    window.addEventListener("resize", onResize);
    return () => window.removeEventListener("resize", onResize);
  }, []);

  useEffect(() => {
    if (phase === "loading" && pipelineFinished && result) {
      setPhase("result");
    }
  }, [phase, pipelineFinished, result]);

  useEffect(
    () => () => {
      toastTimers.current.forEach((timer) => clearTimeout(timer));
      toastTimers.current.clear();
    },
    [],
  );

  const handleSubmit = async (payload) => {
    setResult(null);
    setPipelineFinished(false);
    setPhase("loading");

    try {
      const response = await fetch("http://localhost:5000/api/validate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        throw new Error(`Validation API failed: ${response.status}`);
      }

      const data = await response.json();
      setResult(normalizeResult(data));
      pushToast("Validation complete.", "success", 2400);
    } catch {
      await new Promise((resolve) => setTimeout(resolve, 2600));
      setResult(MOCK_RESULT);
      pushToast("Backend unavailable. Showing mock incident data.", "warning", 4200);
    }
  };

  const handleReset = () => {
    setPhase("input");
    setResult(null);
    setPipelineFinished(false);
    setToasts([]);
    toastTimers.current.forEach((timer) => clearTimeout(timer));
    toastTimers.current.clear();
  };

  return (
    <>
      <link
        href="https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap"
        rel="stylesheet"
      />
      <Scanlines />
      <ToastStack toasts={toasts} onDismiss={dismissToast} />
      <div
        style={{
          minHeight: "100vh",
          background: "#060910",
          backgroundImage:
            "radial-gradient(ellipse at 20% 50%, #001a0e22 0%, transparent 60%), radial-gradient(ellipse at 80% 20%, #0a001a22 0%, transparent 60%)",
          padding: "0 24px 40px",
          color: "#e6edf3",
          boxSizing: "border-box",
        }}
      >
        <AppHeader phase={phase} onReset={handleReset} />

        <AnimatePresence mode="wait">
          {phase === "input" && (
            <motion.div key="input" exit={{ opacity: 0, y: -20 }}>
              <CompilerForm onSubmit={handleSubmit} />
              <div style={{ maxWidth: 580, margin: "0 auto" }}>
                <IncidentHistory incidents={PAST_INCIDENTS} />
              </div>
            </motion.div>
          )}

          {phase === "loading" && (
            <motion.div key="loading" exit={{ opacity: 0 }}>
              <Pipeline onDone={() => setPipelineFinished(true)} />
            </motion.div>
          )}

          {phase === "result" && result && (
            <motion.div key="result" initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
              <VerdictBanner verdict={result.verdict} />

              <div
                style={{
                  display: "grid",
                  gridTemplateColumns: isNarrow ? "1fr" : "minmax(0,1fr) 300px",
                  gap: 20,
                  alignItems: "start",
                }}
              >
                <div>
                  <Card title="DETECTION DETAILS" delay={0.1} accent="#60a5fa">
                    <CrackTypeBadge crackType={result.crack_type} severity={result.severity} />
                  </Card>

                  <Card title="BINARY DIFF - HEX VIEW" delay={0.2} accent="#f59e0b">
                    <DiffViewer diffs={result.diffs} />
                  </Card>

                  <Card title="RESPONSE ACTIONS" delay={0.3} accent="#00ff9d">
                    <ActionLog actions={result.actions} />
                  </Card>

                  <Card title="INCIDENT REPORT" delay={0.4} accent="#60a5fa">
                    <IncidentReport report={result.report} />
                  </Card>
                </div>

                <div style={{ position: isNarrow ? "static" : "sticky", top: isNarrow ? "auto" : 24 }}>
                  <Card
                    title="TRUST SCORE"
                    delay={0.15}
                    accent={
                      result.trust_score >= 90
                        ? "#00ff9d"
                        : result.trust_score >= 60
                          ? "#f59e0b"
                          : "#ff4d4d"
                    }
                  >
                    <ScoreGauge score={result.trust_score} />
                  </Card>
                  <IncidentHistory incidents={PAST_INCIDENTS} />
                </div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </>
  );
}
