from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from database import get_db
from models import Patient, Appointment

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/ui", response_class=HTMLResponse)
async def ui_home(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "title": "Fake CareCloud API"
    })

@router.get("/ui/patients", response_class=HTMLResponse)
async def ui_patients(request: Request, db: Session = Depends(get_db)):
    patients = db.query(Patient).all()
    
    return templates.TemplateResponse("patients.html", {
        "request": request,
        "title": "Patients",
        "patients": patients
    })

@router.get("/ui/appointments", response_class=HTMLResponse)
async def ui_appointments(request: Request, db: Session = Depends(get_db)):
    appointments = db.query(Appointment).all()
    
    return templates.TemplateResponse("appointments.html", {
        "request": request,
        "title": "Appointments", 
        "appointments": appointments
    })

@router.get("/ui/patients/{patient_id}", response_class=HTMLResponse)
async def ui_patient_detail(request: Request, patient_id: str, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    # Get all appointments for this patient
    appointments = db.query(Appointment).filter(Appointment.patient_id == patient_id).all()
    
    return templates.TemplateResponse("patient_detail.html", {
        "request": request,
        "title": f"Patient: {patient.first_name} {patient.last_name}",
        "patient": patient,
        "appointments": appointments
    })