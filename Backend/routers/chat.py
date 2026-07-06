from fastapi import APIRouter
from schemas.chat import ChatRequest, ChatResponse
from services.langchain_service import ask_career_advice

router=APIRouter(prefix="/chat", tags=["chat"])

@router.post("/ask_career",response_model=ChatResponse)
def ask_career_chatbot(request: ChatRequest):
    response=ask_career_advice(request.session_id,request.message)
    return ChatResponse(response=response)