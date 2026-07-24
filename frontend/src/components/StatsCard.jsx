import { useJob } from "../context/JobContext";

function StatsCard() {
  const { job } = useJob();

  const status = job?.status || "Idle";
  const progress = job?.progress || 0;
  const language = job?.language || "-";
  const duration = job?.duration || "-";

  return (
    <div className="grid">
      <div className="card stat-card">
        <h3>Status</h3>
        <h1>{status}</h1>
      </div>

      <div className="card stat-card">
        <h3>Progress</h3>
        <h1>{progress}%</h1>
      </div>

      <div className="card stat-card">
        <h3>Language</h3>
        <h1>{language}</h1>
      </div>

      <div className="card stat-card">
        <h3>Duration</h3>
        <h1>{duration}</h1>
      </div>
    </div>
  );
}

export default StatsCard;
