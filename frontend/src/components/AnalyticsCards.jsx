import { useMemo } from "react";
import { useJob } from "../context/JobContext";

function AnalyticsCards() {
  const { job } = useJob();

  const analytics = useMemo(() => {
    return {
      progress: job?.progress || 0,
      status: job?.status || "Idle",
      transcript: job?.transcript?.split(" ").length || 0,
      summary: job?.summary?.split(" ").length || 0,
    };
  }, [job]);

  return (
    <div className="analytics-grid">
      <div className="analytics-card">
        <h3>Status</h3>

        <h1>{analytics.status}</h1>
      </div>

      <div className="analytics-card">
        <h3>Progress</h3>

        <h1>{analytics.progress}%</h1>
      </div>

      <div className="analytics-card">
        <h3>Transcript Words</h3>

        <h1>{analytics.transcript}</h1>
      </div>

      <div className="analytics-card">
        <h3>Summary Words</h3>

        <h1>{analytics.summary}</h1>
      </div>
    </div>
  );
}

export default AnalyticsCards;
