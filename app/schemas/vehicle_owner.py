from pydantic import BaseModel, Field, constr
from typing import Pattern  
from uuid import UUID
from datetime import datetime
from enum import Enum


# --- Enum to match SQLAlchemy Enum ---

# --- Base Schema (shared fields) ---
class VehicleOwnerBase(BaseModel):
    organization_id: str | None = None
    full_name: constr = Field(..., min_length=3, max_length=100)
    phone_number: constr = Field(
        ...,
        Pattern=r'^(?:\+91)?[6-9]\d{9}$',
        description="Indian mobile phone number, with optional +91 country code"
    )
    account_status: str
    hashed_password: str
    owner_profile_status: bool = False
    driver_profile: bool = False
    car_profile: bool = False

# --- Output schema ---
class VehicleOwnerOut(VehicleOwnerBase):
    id: UUID
    created_at: datetime

    class Config:
        orm_mode = True
        json_schema_extra = {
            "example": {
                "id": "d290f1ee-6c54-4b01-90e6-d701748f0851",
                "organization_id": "org_123",
                "full_name": "Jane Doe",
                "phone_number": "+12345678901",
                "account_status": "Inactive",
                "owner_profile_status": False,
                "driver_profile": False,
                "car_profile": False,
                "created_at": "2025-08-13T12:00:00Z"
            }
        }
