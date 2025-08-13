# models/vehicle_owner.py
from sqlalchemy import Column, String, TIMESTAMP, Integer, func, Boolean, Enum as SqlEnum
from sqlalchemy.dialects.postgresql import UUID
import uuid
import enum
from app.database.session import Base

class AccountStatusEnum(enum.Enum):
    ACTIVE = "Active"
    INACTIVE = "Inactive"
    PENDING = "Pending"
    
class VehicleOwner(Base):
    __tablename__ = "vehicle_owner"

    # id = Column(Integer, primary_key=True, index=True)
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, index=True)
    organization_id = Column(String)
    full_name = Column(String, nullable=False)
    phone_number = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    account_status = Column(
        SqlEnum(AccountStatusEnum, name="account_status_enum"),
        default=AccountStatusEnum.INACTIVE,
        nullable=False
    )
    created_at = Column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    owner_profile_status = Column(Boolean, nullable=False, default=False)
    driver_profile = Column(Boolean, nullable=False, default=False)
    car_profile = Column(Boolean, nullable=False, default=False)
    
