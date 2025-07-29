from fastapi import APIRouter, Depends, HTTPException, status, Form, Request
from sqlalchemy.orm import Session
from database import get_db
from schemas import TokenResponse, TokenRequest
from auth import create_access_token
import json

router = APIRouter()

@router.post("/oauth2/access_token", response_model=TokenResponse)
async def get_access_token(
    request: Request,
    db: Session = Depends(get_db),
    # Form data parameters (for application/x-www-form-urlencoded)
    grant_type: str = Form(None),
    refresh_token: str = Form(None)
):
    # Check content type to determine how to parse the request
    content_type = request.headers.get("content-type", "")
    
    if "application/json" in content_type:
        # Parse JSON body
        try:
            body = await request.json()
            grant_type = body.get("grant_type")
            refresh_token = body.get("refresh_token")
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid JSON body"
            )
    elif "application/x-www-form-urlencoded" in content_type:
        # Use form data (grant_type and refresh_token already parsed by FastAPI)
        pass
    else:
        # Try to parse as form data anyway for backward compatibility
        if grant_type is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="grant_type is required"
            )
    
    # Validate grant_type
    if not grant_type or grant_type not in ["refresh_token", "authorization_code"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported grant type"
        )
    
    # Generate and return new access token
    access_token = create_access_token(db)
    
    return TokenResponse(
        access_token=access_token,
        token_type="Bearer"
    )