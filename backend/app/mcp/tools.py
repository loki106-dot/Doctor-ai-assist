from datetime import date, timedelta
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.db.models import Doctor, Appointment, Patient


# ---------------------------------------------------
# Doctor Availability
# ---------------------------------------------------

def check_doctor_availability(doctor_name: str, appointment_date: date):
    db: Session = SessionLocal()

    doctor = db.query(Doctor).filter(Doctor.name == doctor_name).first()
    if not doctor:
        return {"error": "Doctor not found"}

    booked_times = (
        db.query(Appointment.time)
        .filter(
            Appointment.doctor_id == doctor.id,
            Appointment.date == appointment_date
        )
        .all()
    )

    booked_times = {t[0].strftime("%H:%M") for t in booked_times}

    all_slots = [
        "09:00", "10:00", "11:00",
        "14:00", "15:00", "16:00"
    ]

    available = [t for t in all_slots if t not in booked_times]

    return {
        "doctor_name": doctor_name,
        "date": appointment_date.isoformat(),
        "available_slots": available
    }


# ---------------------------------------------------
# Appointment Creation
# ---------------------------------------------------

def create_appointment(
    doctor_name: str,
    patient_name: str,
    appointment_date: date,
    appointment_time,
    symptoms: str | None = None
):
    db: Session = SessionLocal()

    doctor = db.query(Doctor).filter(Doctor.name == doctor_name).first()
    patient = db.query(Patient).filter(Patient.name == patient_name).first()

    if not doctor or not patient:
        return {"error": "Doctor or patient not found"}

    appointment = Appointment(
        doctor_id=doctor.id,
        patient_id=patient.id,
        date=appointment_date,
        time=appointment_time,
        symptoms=symptoms
    )

    db.add(appointment)
    db.commit()

    return {
        "status": "success",
        "doctor_name": doctor_name,
        "patient_name": patient_name,
        "date": appointment_date.isoformat(),
        "time": appointment_time.strftime("%H:%M")
    }


# ---------------------------------------------------
# Doctor Stats
# ---------------------------------------------------

def get_doctor_stats(
    doctor_name: str,
    days: int = 1,
    symptom_filter: str | None = None
):
    db: Session = SessionLocal()

    doctor = db.query(Doctor).filter(Doctor.name == doctor_name).first()
    if not doctor:
        return {"error": "Doctor not found"}

    start_date = date.today() - timedelta(days=days)

    q = db.query(Appointment).filter(
        Appointment.doctor_id == doctor.id,
        Appointment.date >= start_date
    )

    if symptom_filter:
        q = q.filter(Appointment.symptoms.ilike(f"%{symptom_filter}%"))

    return {
        "doctor_name": doctor_name,
        "count": q.count()
    }


# ---------------------------------------------------
# ✅ DOCTOR REPORT (FIXED)
# ---------------------------------------------------

def get_doctor_report(doctor_name: str):
    db: Session = SessionLocal()

    doctor = db.query(Doctor).filter(Doctor.name == doctor_name).first()
    if not doctor:
        return {"error": "Doctor not found"}

    today = date.today()
    yesterday = today - timedelta(days=1)
    tomorrow = today + timedelta(days=1)

    yesterday_count = db.query(Appointment).filter(
        Appointment.doctor_id == doctor.id,
        Appointment.date == yesterday
    ).count()

    today_count = db.query(Appointment).filter(
        Appointment.doctor_id == doctor.id,
        Appointment.date == today
    ).count()

    tomorrow_count = db.query(Appointment).filter(
        Appointment.doctor_id == doctor.id,
        Appointment.date == tomorrow
    ).count()

    fever_count = db.query(Appointment).filter(
        Appointment.doctor_id == doctor.id,
        Appointment.symptoms.ilike("%fever%"),
        Appointment.date >= yesterday
    ).count()

    # ✅ THIS FIXES YOUR CRASH
    return {
        "doctor_name": doctor.name,
        "yesterday": yesterday_count,
        "today": today_count,
        "tomorrow": tomorrow_count
        # "fever": fever_count
    }
