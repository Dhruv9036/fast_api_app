import Welcome from "./components/Welcome";
import NavBar from "./components/NavBar";
import CompanyCard from "./components/CompanyCard";
import JobCard from "./components/JobCard";
import Footer from "./components/Footer";
import { useEffect, useState } from "react";
import { getCompanies } from "./Services/CompanyService";
import type { Company } from "./types/company";

function App() {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);
  const [companies, setCompanies] = useState<Company[]>([]);

  async function fetchCompanies() {
    setLoading(true);
    try {
      const companies = await getCompanies();
      setCompanies(companies);
    } catch (error) {
      setError(error as Error);
    } finally {
      setLoading(false);
    }
  }
  
  useEffect(() => {
    fetchCompanies();
  }, []);

  if(error) {
    return <div>Error: {error.message}</div>;
  }

  if(loading) {
    return <div>Loading...</div>;
  }

  return (
    <div>
      <NavBar />
      <Welcome />
      <CompanyCard key={companies.id} companies={companies} />
      <JobCard />
      <Footer />
    </div>
  );
}

export default App;
