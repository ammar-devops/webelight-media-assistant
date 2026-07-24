import { useJob } from "../context/JobContext";

function JobDetails() {
  const { job } = useJob();

  return (
    <div className="card">
      <h2>Job Details</h2>

      <table className="details-table">
        <tbody>
          <tr>
            <td>
              <strong>Job ID</strong>
            </td>
            <td>{job?.job_id || "-"}</td>
          </tr>

          <tr>
            <td>
              <strong>File Name</strong>
            </td>
            <td>{job?.filename || "-"}</td>
          </tr>

          <tr>
            <td>
              <strong>Status</strong>
            </td>
            <td>{job?.status || "-"}</td>
          </tr>

          <tr>
            <td>
              <strong>Progress</strong>
            </td>
            <td>{job?.progress || 0}%</td>
          </tr>

          <tr>
            <td>
              <strong>Language</strong>
            </td>
            <td>{job?.language || "-"}</td>
          </tr>

          <tr>
            <td>
              <strong>Duration</strong>
            </td>
            <td>{job?.duration || "-"}</td>
          </tr>

          <tr>
            <td>
              <strong>Created</strong>
            </td>
            <td>{job?.created_at || "-"}</td>
          </tr>
        </tbody>
      </table>
    </div>
  );
}

export default JobDetails;
