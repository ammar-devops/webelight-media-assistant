import { useState } from "react";
import api from "../api/api";
import { useJob } from "../context/JobContext";

function UploadBox() {
  const { refreshJob } = useJob();

  const [uploading, setUploading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [message, setMessage] = useState("");

  const upload = async (file) => {
    if (!file) return;

    const allowed = [
      "video/mp4",
      "video/quicktime",
      "video/x-msvideo",
      "audio/mpeg",
      "audio/wav",
      "audio/x-wav",
      "audio/mp4",
    ];

    if (!allowed.includes(file.type)) {
      setMessage("Unsupported file type.");
      return;
    }

    const form = new FormData();
    form.append("file", file);

    try {
      setUploading(true);
      setProgress(0);
      setMessage("Uploading...");

      const { data } = await api.post("/upload", form, {
        headers: {
          "Content-Type": "multipart/form-data",
        },

        onUploadProgress: (event) => {
          if (!event.total) return;

          const value = Math.round((event.loaded * 100) / event.total);

          setProgress(value);
        },
      });

      localStorage.setItem("job_id", data.job_id);

      refreshJob();

      setMessage("Upload completed.");
    } catch (err) {
      console.error(err);
      setMessage("Upload failed.");
    } finally {
      setUploading(false);
    }
  };

  const fileSelected = (e) => {
    upload(e.target.files[0]);
  };

  const dragOver = (e) => {
    e.preventDefault();
  };

  const drop = (e) => {
    e.preventDefault();

    if (e.dataTransfer.files.length) {
      upload(e.dataTransfer.files[0]);
    }
  };

  return (
    <div className="card">
      <h2>Upload Media</h2>

      <div className="upload-box" onDragOver={dragOver} onDrop={drop}>
        <input
          id="mediaUpload"
          type="file"
          accept="video/*,audio/*"
          hidden
          onChange={fileSelected}
          disabled={uploading}
        />

        <label htmlFor="mediaUpload">
          <h3>{uploading ? "Uploading..." : "Drag & Drop or Click"}</h3>

          <p>MP4 • MOV • AVI • MP3 • WAV</p>
        </label>
      </div>

      {uploading && (
        <>
          <br />

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
        </>
      )}

      <br />

      <p>{message}</p>
    </div>
  );
}

export default UploadBox;
