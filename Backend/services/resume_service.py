import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.3,
)

resume_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a professional resume analyser.
Analyse the given resume text and provide:
1. Key Skills found
2.Experience Level(Junior/Mid/Senior)
3.Strengths
4.Areas to Improve
5. Suggested Job Roles
Keep the analysis short and structured.
"""),("human","{resune_text}")])