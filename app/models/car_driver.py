# models/car_driver.py
from sqlalchemy import Column, String, Integer, TIMESTAMP
import app.database.session as Base
class CarDriver(Base):
    __tablename__ = "car_driver"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(String)
    full_name = Column(String, nullable=False)
    login_number = Column(String, nullable=False, unique=True)
    contact_number = Column(String, nullable=False, unique=True)
    alternate_number = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
    aadhar_number = Column(String, nullable=False, unique=True)
    aadhar_img_url = Column(String)  # GCS public/signed URL
    address = Column(String)
    driver_status = Column(String)  # Online, Driving, Blocked
    created_at = Column(TIMESTAMP)
