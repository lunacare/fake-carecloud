from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models import Patient, PatientAddress, PatientPhone
from schemas import (
    PatientRequest, PatientCreateResponse, PatientSearchRequest, 
    PatientSearchResponse, PatientResponse
)
from auth import verify_token
import uuid

router = APIRouter()

@router.post("/patients", response_model=PatientCreateResponse)
async def create_patient(
    patient_data: PatientRequest,
    db: Session = Depends(get_db),
    _: bool = Depends(verify_token)
):
    # Create patient
    patient_id = str(uuid.uuid4())
    patient = Patient(
        id=patient_id,
        first_name=patient_data.patient.first_name,
        last_name=patient_data.patient.last_name,
        date_of_birth=patient_data.patient.date_of_birth
    )
    db.add(patient)
    
    # Create addresses
    for addr_data in patient_data.addresses:
        address = PatientAddress(
            patient_id=patient_id,
            line1=addr_data.line1,
            line2=addr_data.line2,
            line3=addr_data.line3 if hasattr(addr_data, 'line3') else None,
            city=addr_data.city,
            state=addr_data.state,
            zip_code=addr_data.zip_code,
            country_name=addr_data.country_name,
            is_primary=addr_data.is_primary
        )
        db.add(address)
    
    # Create phones
    for phone_data in patient_data.phones:
        phone = PatientPhone(
            patient_id=patient_id,
            phone_number=phone_data.phone_number,
            phone_type_code=phone_data.phone_type_code,
            extension=phone_data.extension,
            is_primary=phone_data.is_primary
        )
        db.add(phone)
    
    db.commit()
    
    return PatientCreateResponse(patient=patient_id)

@router.post("/patients/search", response_model=PatientSearchResponse)
async def search_patients(
    search_data: PatientSearchRequest,
    db: Session = Depends(get_db),
    _: bool = Depends(verify_token)
):
    query = db.query(Patient)
    
    # Filter by search criteria
    if search_data.fields.first_name:
        query = query.filter(Patient.first_name.ilike(f"%{search_data.fields.first_name}%"))
    
    if search_data.fields.last_name:
        query = query.filter(Patient.last_name.ilike(f"%{search_data.fields.last_name}%"))
    
    if search_data.fields.date_of_birth:
        query = query.filter(Patient.date_of_birth == search_data.fields.date_of_birth)
    
    patients = query.all()
    
    patient_responses = [
        PatientResponse(
            id=patient.id,
            first_name=patient.first_name,
            last_name=patient.last_name,
            date_of_birth=patient.date_of_birth
        )
        for patient in patients
    ]
    
    return PatientSearchResponse(patients=patient_responses)

@router.get("/patients/{patient_id}", response_model=PatientResponse)
async def get_patient(
    patient_id: str,
    db: Session = Depends(get_db),
    _: bool = Depends(verify_token)
):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found"
        )
    
    return PatientResponse(
        id=patient.id,
        first_name=patient.first_name,
        last_name=patient.last_name,
        date_of_birth=patient.date_of_birth
    )