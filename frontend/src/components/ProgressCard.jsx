import { useJob } from "../context/JobContext";

function ProgressCard() {
  const { job } = useJob();

  const progress = job?.progress ?? 0;
  const status = job?.status ?? "Waiting";

  return (
    <div className="card">
      <h2>Progress</h2>

      <p>{status}</p>

      <div className="progress">
        <div
          className="progress-bar"
          style={{
            width: `${progress}%`,
          }}
        />
      </div>

      <br />

      <strong>{progress}%</strong>
    </div>
  );
}

export default ProgressCard;
