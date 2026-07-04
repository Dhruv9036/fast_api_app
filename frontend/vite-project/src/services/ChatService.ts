import api from "./api";
import type { ChatRequest, ChatResponse } from "../types/Chat";

export const askCareer = async (
  data: ChatRequest
): Promise<ChatResponse> => {
  const response = await api.post<ChatResponse>(
    "/chat/ask_career",
    data
  );

  return response.data;
};