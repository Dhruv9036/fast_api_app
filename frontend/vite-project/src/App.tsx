import NavBar from "./components/NavBar";
import CompanyCard from "./components/CompanyCard";
import JobCard from "./components/JobCard";
import Footer from "./components/Footer";
import { useEffect, useState } from "react";
import { getcompanies, updatecompany, deletecompany, createCompany } from "./services/companyservice";
import { getJobs, updateJob, deleteJob, createJob } from "./services/jobService";
import type { Company } from "./types/company"
import type { Job } from "./types/job"
import Login from "./pages/Login";
import Register from "./pages/Register";
import Chat from "./pages/Chat";
import ResumeAnalyser from "./pages/resumeanalyser";
import JobMatch from "./pages/jobmatch";


function App() {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null)
  const [companies, setCompanies] = useState<Company[]>([]);
  const [jobs, setJobs] = useState<Job[]>([]);
  const [token, setToken] = useState<string | null>(localStorage.getItem("token"));
  const [page, setPage] = useState<"login" | "register">("login");
  const [currentPage, setCurrentPage] = useState("home");

  const handleLogin = (newToken: string) => {
    localStorage.setItem("token", newToken);
    setToken(newToken);
  };

  async function fetchData() {
    setLoading(true);
    try {
      const [companiesData, jobsData] = await Promise.all([
        getCompanies(),
        getJobs()
      ]);
      setCompanies(companiesData);
      setJobs(jobsData);
    } catch (error) {
      setError(Error);
    } finally {
      setLoading(false);
    }
  }

  async function handleEdit(company: Company) {
    try {
      const updatedCompany = await updateCompany(company.id, company);
      setCompanies(prev =>
        prev.map(company =>
          company.id === updatedCompany.id ? updatedCompany : company
        )
      );
    } catch (error) {
      setError(Error);
    }
  }

  async function handleDelete(id: number) {
    try {
      await deleteCompany(id);
      setCompanies(prev =>
        prev.filter(company => company.id !== id)
      );
    } catch (error) {
      setError(Error);
    }
  }

  async function handleAdd(company: Company) {
    try {
      const newCompany = await createCompany(company);
      setCompanies(prev => [...prev, newCompany]);
    } catch (error) {
      setError(Error);
    }
  }

  async function handleJobEdit(job: Job) {
    try {
      const updatedJob = await updateJob(job.id, job);
      setJobs(prev =>
        prev.map(j =>
          j.id === updatedJob.id ? updatedJob : j
        )
      );
    } catch (error) {
      setError(Error);
    }
  }

  async function handleJobDelete(id: number) {
    try {
      await deleteJob(id);
      setJobs(prev =>
        prev.filter(job => job.id !== id)
      );
    } catch (error) {
      setError(Error);
    }
  }

  async function handleJobAdd(job: Job) {
    try {
      const newJob = await createJob(job);
      setJobs(prev => [...prev, newJob]);
    } catch (error) {
      setError(Error);
    }
  }


  useEffect(() => {
    if (token) {
      fetchData();
    }
  }, [token]);

  if (!token) {
    return (
      <>
        {page === "login" ? (
          <Login onLogin={handleLogin} onSwitchToRegister={() => setPage("register")} />
        ) : (
          <Register onSwitchToLogin={() => setPage("login")} />
        )}
      </>
    )
  }

  if (loading) {
    return <div>Loading...</div>
  }

  if (error) {
    return <div>Error: {error.message}</div>
  }
  return (
    <>
      <NavBar CurrentPage={currentPage} onNavigate={setCurrentPage} />
      <br />
      {currentPage === "home" && (
        <>
          <CompanyCard
            companies={companies}
            jobs={jobs}
            onEdit={handleEdit}
            onDelete={handleDelete}
            onAdd={handleAdd}
          />
          <JobCard
            jobs={jobs}
            companies={companies}
            onEdit={handleJobEdit}
            onDelete={handleJobDelete}
            onAdd={handleJobAdd}
          />
        </>
      )}
      {currentPage === "chat" && <Chat />}
      {currentPage === "resume" && <ResumeAnalyser />}
      {currentPage === "jobmatch" && <JobMatch />}
      <footer />
    </>
  )
}

export default App