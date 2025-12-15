from datetime import datetime, timedelta
import os
import pickle

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

SCOPES = ["https://www.googleapis.com/auth/calendar"]


def get_calendar_service():
    creds = None

    if os.path.exists("app/services/token.json"):
        with open("app/services/token.json", "rb") as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "app/services/credentials.json",
                SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open("app/services/token.json", "wb") as token:
            pickle.dump(creds, token)

    return build("calendar", "v3", credentials=creds)


def create_calendar_event(
    doctor_name: str,
    patient_name: str,
    appointment_date,
    appointment_time
):
    service = get_calendar_service()

    start_datetime = datetime.combine(appointment_date, appointment_time)
    end_datetime = start_datetime + timedelta(minutes=30)

    event = {
        "summary": f"Appointment: Dr. {doctor_name} & {patient_name}",
        "description": f"Patient: {patient_name}",
        "start": {
            "dateTime": start_datetime.isoformat(),
            "timeZone": "Asia/Kolkata",
        },
        "end": {
            "dateTime": end_datetime.isoformat(),
            "timeZone": "Asia/Kolkata",
        },
    }

    service.events().insert(calendarId="primary", body=event).execute()
