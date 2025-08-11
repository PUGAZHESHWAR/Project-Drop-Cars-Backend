# models/car_details.py
from sqlalchemy import Column, String, TIMESTAMP, Integer
import app.database.session as Base

class CarDetails(Base):
    __tablename__ = "car_details"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(String)
    car_name = Column(String)
    car_type = Column(String)  # sedan, suv, muv, innova
    car_number = Column(String, nullable=False, unique=True)
    
    rc_front_img_url = Column(String)     # GCS public URL
    rc_back_img_url = Column(String)
    insurance_img_url = Column(String)
    fc_img_url = Column(String)
    car_img_url = Column(String)
    
    car_status = Column(String)  # driving, online, blocked
    created_at = Column(TIMESTAMP)
