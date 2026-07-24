import Navbar from "../components/Navbar";
import AnalyticsCards from "../components/AnalyticsCards";
import UploadBox from "../components/UploadBox";
import ProgressCard from "../components/ProgressCard";
import RecentJobs from "../components/RecentJobs";
import JobDetails from "../components/JobDetails";
import Transcript from "../components/Transcript";
import Summary from "../components/Summary";
import Translation from "../components/Translation";
import Chat from "../components/Chat";
import DownloadCard from "../components/DownloadCard";

function Dashboard() {
  return (
    <>
      <Navbar />

      <AnalyticsCards />

      <div className="grid">
        <UploadBox />

        <ProgressCard />
      </div>

      <RecentJobs />

      <JobDetails />

      <div className="grid">
        <Transcript />

        <Summary />
      </div>

      <div className="grid">
        <Translation />

        <Chat />
      </div>

      <DownloadCard />
    </>
  );
}

export default Dashboard;
