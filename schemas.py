from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# Authentication Schemas
class TokenRequest(BaseModel):
    refresh_token: Optional[str] = None
    grant_type: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "Bearer"

# Provider Schemas
class ProviderSpecialty(BaseModel):
    name: str
    taxonomy: str

class ProviderResponse(BaseModel):
    id: int
    npi: Optional[str] = None
    name: str
    email: Optional[str] = None
    phone_number: Optional[str] = None
    specialty: ProviderSpecialty
    last_name: Optional[str] = None
    first_name: Optional[str] = None

class ProvidersResponse(BaseModel):
    providers: List[ProviderResponse]

# Location Schemas
class LocationAddress(BaseModel):
    line1: Optional[str] = None
    line2: Optional[str] = None
    line3: Optional[str] = None
    city: Optional[str] = None
    zip_code: Optional[str] = None
    county_fips: Optional[str] = None
    county_name: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    state_name: Optional[str] = None
    country_name: Optional[str] = None

class LocationPhone(BaseModel):
    phone_number: str
    phone_type: str
    phone_ext: Optional[str] = None
    is_primary: bool

class LocationResponse(BaseModel):
    id: int
    name: str
    is_visible_appointment_scheduler: bool
    place_of_service_code: Optional[str] = None
    address: LocationAddress
    phones: List[LocationPhone]

class LocationsResponse(BaseModel):
    locations: List[LocationResponse]

# Appointment Resource Schemas
class AppointmentResourceDetail(BaseModel):
    id: int
    business_entity_id: str
    name: str
    code: Optional[str] = None
    description: Optional[str] = None
    status: str
    sort_code: int
    created_at: str
    updated_at: str
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
    is_for_requests: bool
    appointment_confirmation: str

class AppointmentResourceResponse(BaseModel):
    resource: AppointmentResourceDetail

# Visit Reason Schemas
class VisitReasonResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

# Patient Schemas
class PatientAddress(BaseModel):
    line1: str
    line2: Optional[str] = ""
    line3: Optional[str] = ""
    city: str
    state: str
    zip_code: str
    country_name: str = "USA"
    is_primary: bool = True

class PatientPhone(BaseModel):
    phone_number: str
    phone_type_code: str = "M"
    extension: Optional[str] = ""
    is_primary: bool = True

class PatientCreate(BaseModel):
    first_name: str
    last_name: str
    date_of_birth: str

class PatientRequest(BaseModel):
    patient: PatientCreate
    addresses: List[PatientAddress]
    phones: List[PatientPhone]

class PatientResponse(BaseModel):
    id: str
    first_name: str
    last_name: str
    date_of_birth: str

class PatientCreateResponse(BaseModel):
    patient: str

class PatientSearchRequest(BaseModel):
    fields: PatientCreate

class PatientSearchResponse(BaseModel):
    patients: List[PatientResponse]

# Appointment Schemas
class AppointmentPatient(BaseModel):
    id: str

class AppointmentCreate(BaseModel):
    start_time: str
    end_time: str
    provider_id: int
    location_id: int
    visit_reason_id: int
    resource_id: int
    patient: AppointmentPatient

class AppointmentRequest(BaseModel):
    appointment: AppointmentCreate

class AppointmentResponse(BaseModel):
    id: str
    start_time: str
    end_time: str
    provider_id: int
    location_id: int
    visit_reason_id: int
    resource_id: int
    patient_id: str
    status: str

class AppointmentCreateResponse(BaseModel):
    appointment: str