from pydantic import BaseModel, EmailStr
from datetime import datetime
from .models import RoleEnum, AppointmentStatus

# ------------------------------
# Registration / Login schemas
# ------------------------------

class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: RoleEnum

    class Config:
        from_attributes = True  # Pydantic v2 replacement for orm_mode

class LoginSchema(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    # expires_in: int | None = None  # optional

    class Config:
        from_attributes = True

# ------------------------------
# User schemas
# ------------------------------

class UserCreate(RegisterRequest):
    """Reuses RegisterRequest for DB creation"""
    pass

class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: RoleEnum

    class Config:
        from_attributes = True

# ------------------------------
# Appointment schemas
# ------------------------------

class AppointmentCreate(BaseModel):
    doctor_id: int
    timestamp: datetime

class AppointmentOut(BaseModel):
    id: int
    patient_id: int
    doctor_id: int
    status: AppointmentStatus
    timestamp: datetime

    class Config:
        from_attributes = True

# ------------------------------
# Doctor Status schemas
# ------------------------------

class StatusSetRequest(BaseModel):
    status: str  # e.g., "online", "offline", "busy"

class StatusOut(BaseModel):
    doctor_id: int
    status: str
