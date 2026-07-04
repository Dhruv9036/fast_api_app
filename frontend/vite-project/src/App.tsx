// import Welcome from "./components/Welcome";
import NavBar from "./components/NavBar";
import CompanyCard from "./components/CompanyCard";
import JobCard from "./components/JobCard";
import Footer from "./components/Footer";
import { useEffect, useState } from "react";
import { getcompanies, updatecompany, deletecompany, createcompany } from "./services/companyservice";
import { getJobs, updateJob, deleteJob, createJob } from "./services/jobservice";
import type { Company } from "./types/company"
import type { Job } from "./types/job"
import Login from "./pages/login";
import Register from "./pages/Register";
import Chat from "./pages/Chat";

function App() {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null)
  const [companies, setCompanies] = useState<Company[]>([]);
  const [jobs, setJobs] = useState<Job[]>([]);
  const [token, setToken] = useState<string | null>(localStorage.getItem("token"));
  const [page, setPage] = useState<"login" | "register">("login");

  const handleLogin = (newToken: string) => {
    localStorage.setItem("token", newToken);
    setToken(newToken);
  };

  async function fetchData() {
    setLoading(true);
    try {
      const [companiesData, jobsData] = await Promise.all([
        getcompanies(),
        getJobs()
      ]);
      setCompanies(companiesData);
      setJobs(jobsData);
    } catch (err) {
      setError(err instanceof Error ? err : new Error(String(err)));
    } finally {
      setLoading(false);
    }
  }

  async function handleEdit(company: Company) {
    try {
      const updatedCompany = await updatecompany(company.id, company);
      setCompanies(prev =>
        prev.map(company =>
          company.id === updatedCompany.id ? updatedCompany : company
        )
      );
    } catch (err) {
      setError(err instanceof Error ? err : new Error(String(err)));
    }
  }

  async function handleDelete(id: number) {
    try {
      await deletecompany(id);
      setCompanies(prev =>
        prev.filter(company => company.id !== id)
      );
    } catch (err) {
      setError(err instanceof Error ? err : new Error(String(err)));
    }
  }

  async function handleAdd(company: Company) {
    try {
      const newCompany = await createcompany(company);
      setCompanies(prev => [...prev, newCompany]);
    } catch (err) {
      setError(err instanceof Error ? err : new Error(String(err)));
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
    } catch (err) {
      setError(err instanceof Error ? err : new Error(String(err)));
    }
  }

  async function handleJobDelete(id: number) {
    try {
      await deleteJob(id);
      setJobs(prev =>
        prev.filter(job => job.id !== id)
      );
    } catch (err) {
      setError(err instanceof Error ? err : new Error(String(err)));
    }
  }

  async function handleJobAdd(job: Job) {
    try {
      const newJob = await createJob(job);
      setJobs(prev => [...prev, newJob]);
    } catch (err) {
      setError(err instanceof Error ? err : new Error(String(err)));
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
      <NavBar />
      {/* <Welcome /> */}
      <br />
      <Chat />
      <br />
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
      <footer />
    </>
  )
}

export default App