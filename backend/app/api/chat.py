from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional
import re

from app.core.agent import run_agent, book_appointment_backend

router = APIRouter()


class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    user_role: str
    messages: List[Message]
    patient_name: Optional[str] = None
    doctor_name: Optional[str] = None


def extract_doctor_from_messages(messages: List[Message]) -> Optional[str]:
    """
    Extract doctor name like 'Dr. Ram' from chat history
    """
    for msg in reversed(messages):
        match = re.search(r"dr\.?\s+([a-zA-Z]+)", msg.content, re.IGNORECASE)
        if match:
            return match.group(1).capitalize()
    return None


@router.post("/chat")
def chat(request: ChatRequest):
    last_user_msg = request.messages[-1].content.lower()

    # -------------------------------------------------
    # 📌 BOOKING TRIGGER (explicit)
    # -------------------------------------------------
    time_match = re.search(r"(\d{1,2}(:\d{2})?\s*(am|pm))", last_user_msg)

    if "book" in last_user_msg and time_match:
        time_str = time_match.group(1)

        patient_name = request.patient_name
        doctor_name = request.doctor_name or extract_doctor_from_messages(
            request.messages
        )

        if not patient_name or not doctor_name:
            return {
                "reply": "❌ Doctor or patient information is missing. Please refresh and try again."
            }

        result = book_appointment_backend(
            doctor_name=doctor_name,
            patient_name=patient_name,
            appointment_date="tomorrow",
            appointment_time=time_str,
            symptoms=None
        )

        return {
            "reply": f"✅ Your appointment with Dr. {doctor_name} has been confirmed for {time_str} tomorrow.\n"
                     "📧 A confirmation email has been sent and 📅 the event has been added to the calendar."
        }

    # -------------------------------------------------
    # 🤖 NORMAL AI FLOW
    # -------------------------------------------------
    reply = run_agent(
        role=request.user_role,
        messages=[m.dict() for m in request.messages],
        patient_name=request.patient_name,
        doctor_name=request.doctor_name
    )

    return {"reply": reply}
