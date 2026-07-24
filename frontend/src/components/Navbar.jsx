import { useJob } from "../context/JobContext";

function Navbar() {
  const { job } = useJob();

  const status = job?.status || "Idle";

  const getColor = () => {
    switch (status) {
      case "queued":
        return "#f59e0b";

      case "processing":
        return "#3b82f6";

      case "completed":
        return "#22c55e";

      case "failed":
        return "#ef4444";

      default:
        return "#6b7280";
    }
  };

  return (
    <div className="navbar">
      <div>
        <div className="logo">🎬 AI Media Assistant</div>

        <small>Audio • Video • Transcript • Summary • AI Chat</small>
      </div>

      <div
        className="status"
        style={{
          background: getColor(),
        }}
      >
        {status.toUpperCase()}
      </div>
    </div>
  );
}

export default Navbar;
