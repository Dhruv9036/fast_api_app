import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.runnables import chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables import RunnableWithMessageHistory

load_dotenv()

llm=ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("API_KEY"),
    temperature=0.7,
)

prompt_with_memory = ChatPromptTemplate.from_messages([
    ("system", "you are a helpful assistant"),
    ("placeholder", "{chat_history}"),
    ("human", "{user_query}")
])

chain_with_memory = prompt_with_memory | llm

store={}

def get_history(session_id: str):
    if session_id not in store:
        store[session_id]=ChatMessageHistory()
    return store[session_id]

chat_with_memory=RunnableWithMessageHistory(
    runnable=chain_with_memory,
    get_session_history=get_history,
    input_messages_key="user_query",
    message_history="chat_history"
)

def ask_career_advice(session_id: str, user_query: str):
    response = chat_with_memory.invoke({"user_query": user_query}, {"configurable": {"session_id": session_id}})
    return response.content