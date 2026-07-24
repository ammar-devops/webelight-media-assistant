import { useState } from "react";
import api from "../api/api";
import { useJob } from "../context/JobContext";

function Translation() {
  const { job } = useJob();

  const [language, setLanguage] = useState("Hindi");
  const [translation, setTranslation] = useState("");
  const [loading, setLoading] = useState(false);

  const translate = async () => {
    if (!job?.job_id) {
      alert("Please upload a file first.");
      return;
    }

    try {
      setLoading(true);

      const { data } = await api.post("/translate/", {
        job_id: job.job_id,
        target_language: language,
      });

      if (data.success) {
        setTranslation(data.translation);
      } else {
        alert("Translation failed.");
      }
    } catch (error) {
      console.error(error);

      alert(
        error?.response?.data?.detail || error.message || "Translation failed.",
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card">
      <h2>Translation</h2>

      <select value={language} onChange={(e) => setLanguage(e.target.value)}>
        <option>Hindi</option>
        <option>English</option>
        <option>Gujarati</option>
        <option>Arabic</option>
        <option>French</option>
        <option>German</option>
      </select>

      <br />
      <br />

      <button onClick={translate} disabled={loading || !job}>
        {loading ? "Translating..." : "Translate"}
      </button>

      <br />
      <br />

      <textarea
        rows={10}
        readOnly
        value={translation}
        placeholder="Translated text will appear here..."
      />
    </div>
  );
}

export default Translation;
