from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from models import AuthToken
from database import get_db
from datetime import datetime, timedelta
import secrets

security = HTTPBearer()

def generate_access_token() -> str:
    return secrets.token_urlsafe(32)

def create_access_token(db: Session) -> str:
    # Generate new token
    access_token = generate_access_token()
    expires_at = datetime.utcnow() + timedelta(hours=1)
    
    # Remove old tokens
    db.query(AuthToken).delete()
    
    # Create new token
    token = AuthToken(
        access_token=access_token,
        expires_at=expires_at
    )
    db.add(token)
    db.commit()
    
    return access_token

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    token = credentials.credentials
    
    # Check if token exists and is not expired
    db_token = db.query(AuthToken).filter(
        AuthToken.access_token == token,
        AuthToken.expires_at > datetime.utcnow()
    ).first()
    
    if not db_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return True