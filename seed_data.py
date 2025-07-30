import logging
from sqlalchemy.orm import Session
from models import (
    Provider, Location, AppointmentResource, VisitReason, 
    Patient, PatientAddress, PatientPhone
)
from datetime import datetime, timedelta
import uuid

logger = logging.getLogger("fake_carecloud.seed_data")

def create_seed_data(db: Session):
    # Check if data already exists
    if db.query(Provider).first():
        logger.info("Seed data already exists, skipping initialization")
        return
    
    logger.info("Creating seed data...")
    
    # Create Provider (based on notebook data)
    provider = Provider(
        id=40483,
        npi=None,
        name="Dr. Kris Duggan",
        email=None,
        phone_number="6507223020",
        specialty_name="Single Specialty",
        specialty_taxonomy="193400000X",
        last_name=None,
        first_name=None
    )
    db.add(provider)
    
    # Create Location (based on notebook data)
    location = Location(
        id=55491,
        name="LUNA CARE PHYSICAL THERAPY",
        is_visible_appointment_scheduler=True,
        place_of_service_code="11",
        address_line1="15 CENTURY BLVD STE 300",
        address_line2=None,
        address_line3=None,
        city="NASHVILLE",
        zip_code="37214-3692",
        county_fips="47037",
        county_name="Davidson",
        latitude="36.14568",
        longitude="-86.68619",
        state_name="Tennessee",
        country_name="UNITED STATES",
        phone_number="6507223020",
        phone_type="Main",
        phone_ext=None,
        is_primary_phone=True
    )
    db.add(location)
    
    # Create Appointment Resource (based on notebook data)
    resource = AppointmentResource(
        id=37367,
        business_entity_id="fdad613f-20b6-4213-95dd-259bfccbc6a8",
        name="DR. KRIS DUGGAN",
        code=None,
        description=None,
        status="A",
        sort_code=1,
        is_for_requests=True,
        appointment_confirmation="P",
        created_by=1208112,
        updated_by=1208112
    )
    db.add(resource)
    
    # Create Visit Reasons (based on notebook data)
    visit_reasons = [
        VisitReason(id=119107, name="RE-EVALUATION VISIT", description=None),
        VisitReason(id=119106, name="DISCHARGE VISIT", description=None),
        VisitReason(id=119105, name="PROGRESS VISIT", description=None),
        VisitReason(id=119104, name="STANDARD VISIT", description=None),
        VisitReason(id=119103, name="INITIAL VISIT", description=None),
    ]
    for vr in visit_reasons:
        db.add(vr)
    
    # No sample patients created - API starts with empty patient database
    
    db.commit()
    logger.info("Seed data created successfully!")