import json
import os
from datetime import datetime, timedelta, time
from dotenv import load_dotenv
from groq import Groq

from app.mcp.tools import (
    check_doctor_availability,
    create_appointment,
    get_doctor_stats,
    get_doctor_report
)

from app.services.slack_service import send_slack_message

from app.core.prompts import (
    PATIENT_SYSTEM_PROMPT,
    DOCTOR_SYSTEM_PROMPT
)

# ------------------------------------------------------------------
# Setup
# ------------------------------------------------------------------

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ------------------------------------------------------------------
# Normalizers
# ------------------------------------------------------------------

def normalize_date(date_str: str) -> str:
    date_str = date_str.lower().strip()

    if date_str == "today":
        return datetime.today().date().isoformat()

    if date_str == "tomorrow":
        return (datetime.today().date() + timedelta(days=1)).isoformat()

    return date_str  # YYYY-MM-DD


def normalize_time(time_str: str) -> str:
    time_str = time_str.strip().upper()

    for fmt in ("%I:%M %p", "%I %p", "%H:%M"):
        try:
            return datetime.strptime(time_str, fmt).time().isoformat(timespec="minutes")
        except ValueError:
            continue

    raise ValueError(f"Invalid time format: {time_str}")

# ------------------------------------------------------------------
# System Prompt
# ------------------------------------------------------------------

def get_system_prompt(role: str):
    return DOCTOR_SYSTEM_PROMPT if role == "doctor" else PATIENT_SYSTEM_PROMPT

# ------------------------------------------------------------------
# TOOLS (ONLY SAFE READ TOOLS)
# ------------------------------------------------------------------

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "check_doctor_availability",
            "description": "Check available appointment slots for a doctor",
            "parameters": {
                "type": "object",
                "properties": {
                    "doctor_name": {"type": "string"},
                    "appointment_date": {"type": "string"}
                },
                "required": ["doctor_name", "appointment_date"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_doctor_stats",
            "description": "Get appointment statistics for a doctor",
            "parameters": {
                "type": "object",
                "properties": {
                    "doctor_name": {"type": "string"},
                    "days": {"type": "integer"},
                    "symptom_filter": {"type": "string"}
                },
                "required": ["doctor_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_doctor_report",
            "description": "Generate a consolidated daily appointment report for a doctor",
            "parameters": {
                "type": "object",
                "properties": {
                    "doctor_name": {"type": "string"}
                },
                "required": ["doctor_name"]
            }
        }
    }
]

# ------------------------------------------------------------------
# AGENT
# ------------------------------------------------------------------

def run_agent(
    role: str,
    messages: list,
    patient_name: str | None = None,
    doctor_name: str | None = None
):
    system_prompt = get_system_prompt(role)

    identity = ""
    if role == "patient" and patient_name:
        identity = f"You are a patient named {patient_name}."
    elif role == "doctor" and doctor_name:
        identity = f"You are Dr. {doctor_name}."

    chat_messages = [
        {"role": "system", "content": system_prompt},
        {"role": "system", "content": identity},
        *messages
    ]

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=chat_messages,
        tools=TOOLS,
        tool_choice="auto"
    )

    message = response.choices[0].message

    # --------------------------------------------------------------
    # NORMAL CHAT (NO TOOL)
    # --------------------------------------------------------------
    if not message.tool_calls:
        return message.content

    # --------------------------------------------------------------
    # TOOL CALL (SANITIZED)
    # --------------------------------------------------------------
    tool_call = message.tool_calls[0]
    args = json.loads(tool_call.function.arguments)
    tool_name = tool_call.function.name

    # ✅ Normalize doctor name ONCE
    doctor = args.get("doctor_name", "")
    doctor = doctor.replace("Dr.", "").replace("Dr", "").strip()

    # ----------------- CHECK AVAILABILITY -------------------------
    if tool_name == "check_doctor_availability":
        date_iso = normalize_date(args["appointment_date"])

        result = check_doctor_availability(
            doctor,
            datetime.fromisoformat(date_iso).date()
        )

    # ----------------- DOCTOR STATS -------------------------------
    elif tool_name == "get_doctor_stats":
        result = get_doctor_stats(
            doctor,
            args.get("days", 1),
            args.get("symptom_filter")
        )

    # ----------------- DOCTOR REPORT (SLACK) ----------------------
    elif tool_name == "get_doctor_report":
        report = get_doctor_report(doctor)

        formatted = f"""
📊 *Daily Summary – Dr. {report['doctor_name']}*

• Patients visited yesterday: {report['yesterday']}
• Appointments today: {report['today']}
• Appointments tomorrow: {report['tomorrow']}
• Fever cases (last 24h): {report['fever']}
""".strip()

        send_slack_message(formatted)

        # ✅ IMPORTANT: return clean response to frontend
        return "✅ Daily report has been generated and sent to Slack."

    else:
        result = {"error": "Unknown tool"}

    # --------------------------------------------------------------
    # SEND TOOL RESULT BACK TO LLM
    # --------------------------------------------------------------
    followup = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            *chat_messages,
            message,
            {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(result)
            }
        ]
    )

    return followup.choices[0].message.content

# ------------------------------------------------------------------
# MANUAL BOOKING (CALLED FROM chat.py)
# ------------------------------------------------------------------

def book_appointment_backend(
    doctor_name: str,
    patient_name: str,
    appointment_date: str,
    appointment_time: str,
    symptoms: str | None = None
):
    date_iso = normalize_date(appointment_date)
    time_iso = normalize_time(appointment_time)

    return create_appointment(
        doctor_name=doctor_name.replace("Dr.", "").replace("Dr", "").strip(),
        patient_name=patient_name,
        appointment_date=datetime.fromisoformat(date_iso).date(),
        appointment_time=time.fromisoformat(time_iso),
        symptoms=symptoms
    )
