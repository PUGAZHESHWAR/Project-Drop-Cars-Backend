from pydantic import BaseModel
from enum import Enum

class AccountStatusEnum(str, Enum):
    ACTIVE = "Active"
    INACTIVE = "Inactive"
    PENDING = "Pending"

class UserCreate(BaseModel):
    full_name: str
    mobile_number: str
    password: str

class UserLogin(BaseModel):
    mobile_number: str
    password: str