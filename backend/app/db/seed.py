from sqlalchemy.orm import Session
from app.db.database import engine, SessionLocal
from app.db.models import Base, Doctor, Patient


def create_tables():
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully")


def seed_data():
    db: Session = SessionLocal()

    # Avoid duplicate inserts
    if db.query(Doctor).first():
        print("Data already exists. Skipping seeding.")
        db.close()
        return

    doctors = [
        Doctor(name="Ahuja", specialization="General"),
        Doctor(name="Ram", specialization="Cardiology"),
        Doctor(name="Bala", specialization="Dermatology"),
    ]

    patients = [
        Patient(name="Patient1", email="light.yagami.ly2@gmail.com"),
        Patient(name="Patient2", email="light.yagami.ly2@gmail.com"),
        Patient(name="Patient3", email="light.yagami.ly2@gmail.com"),
    ]

    db.add_all(doctors + patients)
    db.commit()
    db.close()

    print("Dummy data inserted successfully")


if __name__ == "__main__":
    create_tables()
    seed_data()
