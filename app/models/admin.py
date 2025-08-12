# app/models/admin.py
from sqlalchemy import Column, Integer, String, TIMESTAMP
from database.session import Base

class Admin(Base):
    __tablename__ = "admin"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    password = Column(String)
    role = Column(String)  # Owner, Manager
    email = Column(String)
    phone = Column(String)
    organization_id = Column(String)
    created_at = Column(TIMESTAMP)
