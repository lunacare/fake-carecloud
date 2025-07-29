from sqlalchemy import Column, String, Integer, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime
import uuid

class Provider(Base):
    __tablename__ = "providers"
    
    id = Column(Integer, primary_key=True, index=True)
    npi = Column(String(50), nullable=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=True)
    phone_number = Column(String(50), nullable=True)
    specialty_name = Column(String(255), nullable=True)
    specialty_taxonomy = Column(String(50), nullable=True)
    last_name = Column(String(255), nullable=True)
    first_name = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Location(Base):
    __tablename__ = "locations"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    is_visible_appointment_scheduler = Column(Boolean, default=True)
    place_of_service_code = Column(String(10), nullable=True)
    address_line1 = Column(String(255), nullable=True)
    address_line2 = Column(String(255), nullable=True)
    address_line3 = Column(String(255), nullable=True)
    city = Column(String(100), nullable=True)
    zip_code = Column(String(20), nullable=True)
    county_fips = Column(String(10), nullable=True)
    county_name = Column(String(100), nullable=True)
    latitude = Column(String(50), nullable=True)
    longitude = Column(String(50), nullable=True)
    state_name = Column(String(100), nullable=True)
    country_name = Column(String(100), nullable=True)
    phone_number = Column(String(50), nullable=True)
    phone_type = Column(String(50), default="Main")
    phone_ext = Column(String(20), nullable=True)
    is_primary_phone = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class AppointmentResource(Base):
    __tablename__ = "appointment_resources"
    
    id = Column(Integer, primary_key=True, index=True)
    business_entity_id = Column(String(100), nullable=True)
    name = Column(String(255), nullable=False)
    code = Column(String(50), nullable=True)
    description = Column(Text, nullable=True)
    status = Column(String(10), default="A")
    sort_code = Column(Integer, default=1)
    is_for_requests = Column(Boolean, default=True)
    appointment_confirmation = Column(String(10), default="P")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    created_by = Column(Integer, nullable=True)
    updated_by = Column(Integer, nullable=True)

class VisitReason(Base):
    __tablename__ = "visit_reasons"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)

class Patient(Base):
    __tablename__ = "patients"
    
    id = Column(String(100), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    date_of_birth = Column(String(20), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    
    addresses = relationship("PatientAddress", back_populates="patient")
    phones = relationship("PatientPhone", back_populates="patient")
    appointments = relationship("Appointment", back_populates="patient")

class PatientAddress(Base):
    __tablename__ = "patient_addresses"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(String(100), ForeignKey("patients.id"))
    line1 = Column(String(255), nullable=False)
    line2 = Column(String(255), nullable=True)
    line3 = Column(String(255), nullable=True)
    city = Column(String(100), nullable=False)
    state = Column(String(50), nullable=False)
    zip_code = Column(String(20), nullable=False)
    country_name = Column(String(100), default="USA")
    is_primary = Column(Boolean, default=True)
    
    patient = relationship("Patient", back_populates="addresses")

class PatientPhone(Base):
    __tablename__ = "patient_phones"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(String(100), ForeignKey("patients.id"))
    phone_number = Column(String(50), nullable=False)
    phone_type_code = Column(String(10), default="M")
    extension = Column(String(20), nullable=True)
    is_primary = Column(Boolean, default=True)
    
    patient = relationship("Patient", back_populates="phones")

class Appointment(Base):
    __tablename__ = "appointments"
    
    id = Column(String(100), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    provider_id = Column(Integer, ForeignKey("providers.id"))
    location_id = Column(Integer, ForeignKey("locations.id"))
    visit_reason_id = Column(Integer, ForeignKey("visit_reasons.id"))
    resource_id = Column(Integer, ForeignKey("appointment_resources.id"))
    patient_id = Column(String(100), ForeignKey("patients.id"))
    status = Column(String(50), default="scheduled")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    
    provider = relationship("Provider")
    location = relationship("Location")
    visit_reason = relationship("VisitReason")
    resource = relationship("AppointmentResource")
    patient = relationship("Patient", back_populates="appointments")

class AuthToken(Base):
    __tablename__ = "auth_tokens"
    
    id = Column(Integer, primary_key=True, index=True)
    access_token = Column(String(255), nullable=False, unique=True)
    token_type = Column(String(50), default="Bearer")
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)