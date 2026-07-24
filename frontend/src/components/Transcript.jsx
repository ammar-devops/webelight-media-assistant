import { useJob } from "../context/JobContext";

function Transcript() {
  const { job } = useJob();

  return (
    <div className="card">
      <h2>Transcript</h2>

      <textarea readOnly value={job?.transcript || ""} />
    </div>
  );
}

export default Transcript;
