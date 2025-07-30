from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Patient, Appointment
from schemas import PatientResponse, AppointmentResponse
from typing import List

router = APIRouter()

@router.get("/patients", response_model=List[PatientResponse])
async def debug_patients(db: Session = Depends(get_db)):
    """Debug endpoint to return all patients in the database."""
    patients = db.query(Patient).all()
    return patients

@router.get("/appointments", response_model=List[AppointmentResponse])
async def debug_appointments(db: Session = Depends(get_db)):
    """Debug endpoint to return all appointments in the database."""
    appointments = db.query(Appointment).all()
    return appointments