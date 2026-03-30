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
import { normalizeResult } from "./utils/normalizeResult";

const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL || "http://localhost:5000").replace(/\/$/, "");

function toRelativeTime(timestamp) {
  if (!timestamp) {
    return "unknown";
  }

  const parsed = new Date(timestamp);
  if (Number.isNaN(parsed.getTime())) {
    return "unknown";
  }

  const diffMs = Date.now() - parsed.getTime();
  const diffMinutes = Math.floor(diffMs / 60000);
  if (diffMinutes < 1) {
    return "just now";
  }
  if (diffMinutes < 60) {
    return `${diffMinutes}m ago`;
  }

  const diffHours = Math.floor(diffMinutes / 60);
  if (diffHours < 24) {
    return `${diffHours}h ago`;
  }

  const diffDays = Math.floor(diffHours / 24);
  return `${diffDays}d ago`;
}

function mapIncident(raw, index) {
  const timestamp = raw.timestamp || raw.time || raw.created_at || null;
  return {
    id: raw.id || raw.incident_id || `INC-${index + 1}`,
    verdict: raw.verdict || "SUSPICIOUS",
    score: Number.isFinite(raw.trust_score) ? raw.trust_score : raw.score,
    type: raw.crack_type || "unknown",
    time: toRelativeTime(timestamp),
  };
}

export default function App() {
  const [phase, setPhase] = useState("input");
  const [result, setResult] = useState(null);
  const [pipelineFinished, setPipelineFinished] = useState(false);
  const [isNarrow, setIsNarrow] = useState(() => window.innerWidth < 1080);
  const [toasts, setToasts] = useState([]);
  const [incidents, setIncidents] = useState([]);
  const [incidentError, setIncidentError] = useState("");
  const toastTimers = useRef(new Map());

  const loadIncidents = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/incidents`);
      if (!response.ok) {
        throw new Error(`Incident API failed: ${response.status}`);
      }
      const data = await response.json();
      if (!Array.isArray(data)) {
        throw new Error("Incident API returned invalid payload");
      }
      setIncidents(data.map(mapIncident));
      setIncidentError("");
    } catch (error) {
      const message = error instanceof Error ? error.message : "Unable to load incidents";
      setIncidentError(message);
    }
  };

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

  useEffect(() => {
    loadIncidents();
    const interval = setInterval(loadIncidents, 15000);
    return () => clearInterval(interval);
  }, []);

  const handleSubmit = async (payload) => {
    setResult(null);
    setPipelineFinished(false);
    setPhase("loading");

    try {
      const response = await fetch(`${API_BASE_URL}/api/validate`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          source_path: payload.source,
          suspect_compiler: payload.suspect,
          trusted_compiler: payload.trusted,
        }),
      });

      if (!response.ok) {
        throw new Error(`Validation API failed: ${response.status}`);
      }

      const data = await response.json();
      if (data?.error) {
        throw new Error(data.error);
      }

      const normalized = normalizeResult(data);
      if (!normalized) {
        throw new Error("Validation API returned invalid response");
      }

      setResult(normalized);
      await loadIncidents();
      pushToast("Validation complete.", "success", 2400);
    } catch (error) {
      setPhase("input");
      setPipelineFinished(false);
      const message = error instanceof Error ? error.message : "Unknown error";
      pushToast(`Validation failed: ${message}`, "warning", 4200);
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
                <IncidentHistory incidents={incidents} />
                {incidentError && (
                  <div
                    style={{
                      fontFamily: "'Share Tech Mono', monospace",
                      fontSize: 11,
                      color: "#f59e0b",
                      marginTop: 10,
                    }}
                  >
                    Live incident stream unavailable: {incidentError}
                  </div>
                )}
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
                  <IncidentHistory incidents={incidents} />
                </div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </>
  );
}
