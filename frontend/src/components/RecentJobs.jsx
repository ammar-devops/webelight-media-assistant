import { useEffect, useState } from "react";
import api from "../api/api";
import SearchBar from "./SearchBar";

function RecentJobs() {
  const [jobs, setJobs] = useState([]);
  const [filtered, setFiltered] = useState([]);

  const loadJobs = async () => {
    try {
      const { data } = await api.get("/jobs");

      const list = data.jobs || data || [];

      setJobs(list);

      setFiltered(list);
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    loadJobs();
  }, []);

  const search = (text) => {
    const value = text.toLowerCase();

    setFiltered(
      jobs.filter((job) => job.filename.toLowerCase().includes(value)),
    );
  };

  return (
    <div className="card">
      <h2>Recent Jobs</h2>

      <SearchBar onSearch={search} />

      <table className="jobs-table">
        <thead>
          <tr>
            <th>Filename</th>

            <th>Status</th>

            <th>Progress</th>
          </tr>
        </thead>

        <tbody>
          {filtered.map((job) => (
            <tr key={job.job_id}>
              <td>{job.filename}</td>

              <td>{job.status}</td>

              <td>{job.progress}%</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default RecentJobs;
