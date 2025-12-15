from pydantic import BaseModel
from typing import Optional, List
from datetime import date, time


class AvailabilityRequest(BaseModel):
    doctor_name: str
    date: date


class AvailabilityResponse(BaseModel):
    available_slots: List[str]


class AppointmentRequest(BaseModel):
    doctor_name: str
    patient_name: str
    date: date
    time: time
    symptoms: Optional[str] = None


class AppointmentResponse(BaseModel):
    status: str
    message: str


class DoctorStatsRequest(BaseModel):
    doctor_name: str
    days: int = 1
    symptom_filter: Optional[str] = None


class DoctorStatsResponse(BaseModel):
    count: int
