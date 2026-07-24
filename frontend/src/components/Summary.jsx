import { useJob } from "../context/JobContext";

function Summary() {
  const { job } = useJob();

  return (
    <div className="card">
      <h2>Summary</h2>

      <textarea readOnly value={job?.summary || ""} />
    </div>
  );
}

export default Summary;
