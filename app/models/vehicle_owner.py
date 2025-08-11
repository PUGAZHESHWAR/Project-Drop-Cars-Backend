# models/vehicle_owner.py
from sqlalchemy import Column, String, TIMESTAMP, Integer
from app.database.session import Base
class VehicleOwner(Base):
    __tablename__ = "vehicle_owner"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(String)
    phone_number = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    account_status = Column(String)
    created_at = Column(TIMESTAMP)
