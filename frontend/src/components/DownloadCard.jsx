import { useJob } from "../context/JobContext";
import api from "../api/api";

function DownloadCard() {
  const { job } = useJob();

  const download = async (type) => {
    try {
      const response = await api.get(`/download/${type}/${job.job_id}`, {
        responseType: "blob",
      });

      const url = window.URL.createObjectURL(response.data);

      const a = document.createElement("a");

      a.href = url;

      a.download = `${job.job_id}.${type}`;

      a.click();

      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error(error);
    }
  };

  const disabled = !job || job.status !== "completed";

  return (
    <div className="card">
      <h2>Downloads</h2>

      <div className="downloads">
        <button disabled={disabled} onClick={() => download("pdf")}>
          PDF
        </button>

        <button disabled={disabled} onClick={() => download("docx")}>
          DOCX
        </button>

        <button disabled={disabled} onClick={() => download("txt")}>
          TXT
        </button>

        <button disabled={disabled} onClick={() => download("srt")}>
          SRT
        </button>
      </div>
    </div>
  );
}

export default DownloadCard;
