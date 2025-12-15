from sqlalchemy import Column, Integer, String, Date, Time, ForeignKey
from app.db.database import Base

class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, index=True)
    specialization = Column(String)


class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    email = Column(String)


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True)
    doctor_id = Column(Integer, ForeignKey("doctors.id"))
    patient_id = Column(Integer, ForeignKey("patients.id"))
    date = Column(Date)
    time = Column(Time)
    symptoms = Column(String)
