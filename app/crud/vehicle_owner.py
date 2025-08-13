from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.vehicle_owner import VehicleOwner
from app.schemas.vehicle_owner import VehicleOwnerBase
from app.core.security import get_password_hash, verify_password
from typing import Optional

def create_user(db: Session, user_in: VehicleOwnerBase) -> VehicleOwner:
    existing_user = db.query(VehicleOwner).filter(VehicleOwner.mobile_number == user_in.mobile_number).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User Number already registered")

    hashed_password = get_password_hash(user_in.password)
    db_user = VehicleOwner(
        full_name=user_in.full_name,
        mobile_number=user_in.mobile_number,
        hashed_password=hashed_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# def get_user(db: Session, user_id: int) -> Optional[User]:
#     return db.query(User).filter(User.id == user_id).first()

# def get_user_by_mobile(db: Session, mobile_number: str) -> Optional[User]:
#     return db.query(User).filter(User.mobile_number == mobile_number).first()

# def authenticate_user(db: Session, login_data: UserLogin) -> Optional[User]:
#     user = get_user_by_mobile(db, login_data.mobile_number)
#     if not user or not verify_password(login_data.password, user.hashed_password):
#         return None
#     return user

# def update_user(db: Session, user_id: int, user_update: UserUpdate) -> User:
#     user = get_user(db, user_id)
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")

#     # Update fields except password by default
#     update_data = user_update.dict(exclude_unset=True)
#     if "password" in update_data:
#         update_data["hashed_password"] = get_password_hash(update_data.pop("password"))

#     for key, value in update_data.items():
#         setattr(user, key, value)

#     db.commit()
#     db.refresh(user)
#     return user

# def delete_user(db: Session, user_id: int):
#     user = get_user(db, user_id)
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#     db.delete(user)
#     db.commit()
