import axios from "axios";
import type { Company } from "../types/company";

const API_URL = "http://localhost:8000";

export async function getCompanies(): Promise<Company[]> {
    const response = await axios.get(`${API_URL}/companies`);
    return response.data;
}