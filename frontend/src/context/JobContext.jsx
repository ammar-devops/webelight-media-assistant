import { createContext, useContext, useEffect, useRef, useState } from "react";
import api from "../api/api";

const JobContext = createContext();

export function JobProvider({ children }) {
  const [job, setJob] = useState(null);
  const intervalRef = useRef(null);

  const stopPolling = () => {
    if (intervalRef.current) {
      clearInterval(intervalRef.current);
      intervalRef.current = null;
    }
  };

  const fetchJob = async () => {
    const jobId = localStorage.getItem("job_id");

    if (!jobId) {
      stopPolling();
      return;
    }

    try {
      const { data } = await api.get(`/jobs/${jobId}`);

      setJob(data);

      if (data.status === "completed" || data.status === "failed") {
        stopPolling();
      }
    } catch (error) {
      console.error("Job fetch error:", error);
      stopPolling();
    }
  };

  const refreshJob = async () => {
    await fetchJob();
  };

  useEffect(() => {
    const jobId = localStorage.getItem("job_id");

    if (!jobId) return;

    fetchJob();

    intervalRef.current = setInterval(() => {
      fetchJob();
    }, 3000);

    return () => {
      stopPolling();
    };
  }, []);

  return (
    <JobContext.Provider
      value={{
        job,
        refreshJob,
      }}
    >
      {children}
    </JobContext.Provider>
  );
}

export function useJob() {
  return useContext(JobContext);
}
