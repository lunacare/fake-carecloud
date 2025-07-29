from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models import Appointment, Patient
from schemas import (
    AppointmentRequest, AppointmentCreateResponse, AppointmentResponse
)
from auth import verify_token
from datetime import datetime
import uuid

router = APIRouter()

@router.post("/appointments", response_model=AppointmentCreateResponse)
async def create_appointment(
    appointment_data: AppointmentRequest,
    db: Session = Depends(get_db),
    _: bool = Depends(verify_token)
):
    # Verify patient exists
    patient = db.query(Patient).filter(
        Patient.id == appointment_data.appointment.patient.id
    ).first()
    
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Patient not found"
        )
    
    # Parse datetime strings
    try:
        start_time = datetime.fromisoformat(appointment_data.appointment.start_time.replace('Z', '+00:00'))
        end_time = datetime.fromisoformat(appointment_data.appointment.end_time.replace('Z', '+00:00'))
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid datetime format"
        )
    
    # Create appointment
    appointment_id = str(uuid.uuid4())
    appointment = Appointment(
        id=appointment_id,
        start_time=start_time,
        end_time=end_time,
        provider_id=appointment_data.appointment.provider_id,
        location_id=appointment_data.appointment.location_id,
        visit_reason_id=appointment_data.appointment.visit_reason_id,
        resource_id=appointment_data.appointment.resource_id,
        patient_id=appointment_data.appointment.patient.id,
        status="scheduled"
    )
    
    db.add(appointment)
    db.commit()
    
    return AppointmentCreateResponse(appointment=appointment_id)

@router.get("/appointments/{appointment_id}", response_model=AppointmentResponse)
async def get_appointment(
    appointment_id: str,
    db: Session = Depends(get_db),
    _: bool = Depends(verify_token)
):
    appointment = db.query(Appointment).filter(
        Appointment.id == appointment_id
    ).first()
    
    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appointment not found"
        )
    
    return AppointmentResponse(
        id=appointment.id,
        start_time=appointment.start_time.isoformat(),
        end_time=appointment.end_time.isoformat(),
        provider_id=appointment.provider_id,
        location_id=appointment.location_id,
        visit_reason_id=appointment.visit_reason_id,
        resource_id=appointment.resource_id,
        patient_id=appointment.patient_id,
        status=appointment.status
    )

@router.put("/appointments/{appointment_id}", response_model=AppointmentResponse)
async def update_appointment(
    appointment_id: str,
    appointment_data: AppointmentRequest,
    db: Session = Depends(get_db),
    _: bool = Depends(verify_token)
):
    appointment = db.query(Appointment).filter(
        Appointment.id == appointment_id
    ).first()
    
    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appointment not found"
        )
    
    # Parse datetime strings
    try:
        start_time = datetime.fromisoformat(appointment_data.appointment.start_time.replace('Z', '+00:00'))
        end_time = datetime.fromisoformat(appointment_data.appointment.end_time.replace('Z', '+00:00'))
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid datetime format"
        )
    
    # Update appointment
    appointment.start_time = start_time
    appointment.end_time = end_time
    appointment.provider_id = appointment_data.appointment.provider_id
    appointment.location_id = appointment_data.appointment.location_id
    appointment.visit_reason_id = appointment_data.appointment.visit_reason_id
    appointment.resource_id = appointment_data.appointment.resource_id
    appointment.updated_at = datetime.utcnow()
    
    db.commit()
    
    return AppointmentResponse(
        id=appointment.id,
        start_time=appointment.start_time.isoformat(),
        end_time=appointment.end_time.isoformat(),
        provider_id=appointment.provider_id,
        location_id=appointment.location_id,
        visit_reason_id=appointment.visit_reason_id,
        resource_id=appointment.resource_id,
        patient_id=appointment.patient_id,
        status=appointment.status
    )

@router.delete("/appointments/{appointment_id}")
async def cancel_appointment(
    appointment_id: str,
    db: Session = Depends(get_db),
    _: bool = Depends(verify_token)
):
    appointment = db.query(Appointment).filter(
        Appointment.id == appointment_id
    ).first()
    
    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appointment not found"
        )
    
    # Mark as cancelled instead of deleting
    appointment.status = "cancelled"
    appointment.updated_at = datetime.utcnow()
    
    db.commit()
    
    return {"message": "Appointment cancelled successfully"}