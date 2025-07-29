from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Provider, Location, AppointmentResource, VisitReason
from schemas import (
    ProvidersResponse, ProviderResponse, ProviderSpecialty,
    LocationsResponse, LocationResponse, LocationAddress, LocationPhone,
    AppointmentResourceResponse, AppointmentResourceDetail,
    VisitReasonResponse
)
from auth import verify_token

router = APIRouter()

@router.get("/providers", response_model=ProvidersResponse)
async def get_providers(
    db: Session = Depends(get_db),
    _: bool = Depends(verify_token)
):
    providers = db.query(Provider).all()
    
    provider_responses = [
        ProviderResponse(
            id=provider.id,
            npi=provider.npi,
            name=provider.name,
            email=provider.email,
            phone_number=provider.phone_number,
            specialty=ProviderSpecialty(
                name=provider.specialty_name or "",
                taxonomy=provider.specialty_taxonomy or ""
            ),
            last_name=provider.last_name,
            first_name=provider.first_name
        )
        for provider in providers
    ]
    
    return ProvidersResponse(providers=provider_responses)

@router.get("/locations", response_model=LocationsResponse)
async def get_locations(
    db: Session = Depends(get_db),
    _: bool = Depends(verify_token)
):
    locations = db.query(Location).all()
    
    location_responses = [
        LocationResponse(
            id=location.id,
            name=location.name,
            is_visible_appointment_scheduler=location.is_visible_appointment_scheduler,
            place_of_service_code=location.place_of_service_code,
            address=LocationAddress(
                line1=location.address_line1,
                line2=location.address_line2,
                line3=location.address_line3,
                city=location.city,
                zip_code=location.zip_code,
                county_fips=location.county_fips,
                county_name=location.county_name,
                latitude=float(location.latitude) if location.latitude else None,
                longitude=float(location.longitude) if location.longitude else None,
                state_name=location.state_name,
                country_name=location.country_name
            ),
            phones=[
                LocationPhone(
                    phone_number=location.phone_number or "",
                    phone_type=location.phone_type or "Main",
                    phone_ext=location.phone_ext,
                    is_primary=location.is_primary_phone or True
                )
            ] if location.phone_number else []
        )
        for location in locations
    ]
    
    return LocationsResponse(locations=location_responses)

@router.get("/appointment_resources")
async def get_appointment_resources(
    db: Session = Depends(get_db),
    _: bool = Depends(verify_token)
):
    resources = db.query(AppointmentResource).all()
    
    resource_responses = [
        AppointmentResourceResponse(
            resource=AppointmentResourceDetail(
                id=resource.id,
                business_entity_id=resource.business_entity_id or "",
                name=resource.name,
                code=resource.code,
                description=resource.description,
                status=resource.status,
                sort_code=resource.sort_code,
                created_at=resource.created_at.isoformat() if resource.created_at else "",
                updated_at=resource.updated_at.isoformat() if resource.updated_at else "",
                created_by=resource.created_by,
                updated_by=resource.updated_by,
                is_for_requests=resource.is_for_requests,
                appointment_confirmation=resource.appointment_confirmation
            )
        )
        for resource in resources
    ]
    
    return resource_responses

@router.get("/visit_reasons")
async def get_visit_reasons(
    db: Session = Depends(get_db),
    _: bool = Depends(verify_token)
):
    visit_reasons = db.query(VisitReason).all()
    
    return [
        VisitReasonResponse(
            id=vr.id,
            name=vr.name,
            description=vr.description
        )
        for vr in visit_reasons
    ]