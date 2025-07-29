from fastapi import APIRouter, Depends, Request
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