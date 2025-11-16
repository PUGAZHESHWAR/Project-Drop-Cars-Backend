# crud/admin_management.py
from sqlalchemy.orm import Session
from sqlalchemy import or_
from fastapi import HTTPException, status
from app.models.vendor import VendorCredentials, AccountStatusEnum as VendorAccountStatusEnum
from app.models.vendor_details import VendorDetails
from app.models.vehicle_owner import VehicleOwnerCredentials, AccountStatusEnum as VehicleOwnerAccountStatusEnum
from app.models.vehicle_owner_details import VehicleOwnerDetails
from app.models.car_details import CarDetails, CarStatusEnum
from app.models.car_driver import CarDriver, AccountStatusEnum as DriverStatusEnum
from app.models.common_enums import DocumentStatusEnum
from typing import List, Optional, Tuple
from uuid import UUID

# ============ VENDOR MANAGEMENT ============

def get_all_vendors(db: Session, skip: int = 0, limit: int = 100) -> Tuple[List[VendorDetails], int]:
    """Get all vendors with pagination"""
    vendors = db.query(VendorDetails).offset(skip).limit(limit).all()
    total_count = db.query(VendorDetails).count()
    return vendors, total_count

def get_vendor_full_details(db: Session, vendor_id: str) -> Optional[Tuple[VendorCredentials, VendorDetails]]:
    """Get full vendor details including credentials and details"""
    vendor_credentials = db.query(VendorCredentials).filter(
        VendorCredentials.id == vendor_id
    ).first()
    
    if not vendor_credentials:
        return None
    
    vendor_details = db.query(VendorDetails).filter(
        VendorDetails.vendor_id == vendor_id
    ).first()
    
    return vendor_credentials, vendor_details

def update_vendor_account_status(db: Session, vendor_id: str, account_status: str) -> VendorCredentials:
    """Update vendor account status"""
    vendor = db.query(VendorCredentials).filter(
        VendorCredentials.id == vendor_id
    ).first()
    
    if not vendor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vendor not found"
        )
    
    # Try to match by enum name first (ACTIVE, INACTIVE, PENDING)
    account_status_upper = account_status.upper()
    try:
        vendor.account_status = VendorAccountStatusEnum[account_status_upper]
    except KeyError:
        # Try to match by value (Active, Inactive, Pending)
        for enum_item in VendorAccountStatusEnum:
            if enum_item.value.lower() == account_status.lower():
                vendor.account_status = enum_item
                break
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid account status. Must be one of: {[e.name for e in VendorAccountStatusEnum]} or {[e.value for e in VendorAccountStatusEnum]}"
            )
    
    try:
        db.commit()
        db.refresh(vendor)
        return vendor
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update vendor account status: {str(e)}"
        )

def update_vendor_document_status(db: Session, vendor_id: str, document_status: DocumentStatusEnum) -> VendorDetails:
    """Update vendor document status"""
    vendor_details = db.query(VendorDetails).filter(
        VendorDetails.vendor_id == vendor_id
    ).first()
    
    if not vendor_details:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vendor details not found"
        )
    
    try:
        vendor_details.aadhar_status = document_status
        db.commit()
        db.refresh(vendor_details)
        return vendor_details
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update vendor document status: {str(e)}"
        )

# ============ VEHICLE OWNER MANAGEMENT ============

def get_all_vehicle_owners(db: Session, skip: int = 0, limit: int = 100) -> Tuple[List[VehicleOwnerDetails], int]:
    """Get all vehicle owners with pagination"""
    vehicle_owners = db.query(VehicleOwnerDetails).offset(skip).limit(limit).all()
    total_count = db.query(VehicleOwnerDetails).count()
    return vehicle_owners, total_count

def get_vehicle_owner_full_details(db: Session, vehicle_owner_id: str) -> Optional[Tuple[VehicleOwnerCredentials, VehicleOwnerDetails]]:
    """Get full vehicle owner details including credentials and details"""
    vehicle_owner_credentials = db.query(VehicleOwnerCredentials).filter(
        VehicleOwnerCredentials.id == vehicle_owner_id
    ).first()
    
    if not vehicle_owner_credentials:
        return None
    
    vehicle_owner_details = db.query(VehicleOwnerDetails).filter(
        VehicleOwnerDetails.vehicle_owner_id == vehicle_owner_id
    ).first()
    
    return vehicle_owner_credentials, vehicle_owner_details

def update_vehicle_owner_account_status(db: Session, vehicle_owner_id: str, account_status: str) -> VehicleOwnerCredentials:
    """Update vehicle owner account status"""
    vehicle_owner = db.query(VehicleOwnerCredentials).filter(
        VehicleOwnerCredentials.id == vehicle_owner_id
    ).first()
    
    if not vehicle_owner:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vehicle owner not found"
        )
    
    # Try to match by enum name first (ACTIVE, INACTIVE, PENDING)
    account_status_upper = account_status.upper()
    try:
        vehicle_owner.account_status = VehicleOwnerAccountStatusEnum[account_status_upper]
    except KeyError:
        # Try to match by value (Active, Inactive, Pending)
        for enum_item in VehicleOwnerAccountStatusEnum:
            if enum_item.value.lower() == account_status.lower():
                vehicle_owner.account_status = enum_item
                break
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid account status. Must be one of: {[e.name for e in VehicleOwnerAccountStatusEnum]} or {[e.value for e in VehicleOwnerAccountStatusEnum]}"
            )
    
    try:
        db.commit()
        db.refresh(vehicle_owner)
        return vehicle_owner
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update vehicle owner account status: {str(e)}"
        )

def update_vehicle_owner_document_status(db: Session, vehicle_owner_id: str, document_status: DocumentStatusEnum) -> VehicleOwnerDetails:
    """Update vehicle owner document status"""
    vehicle_owner_details = db.query(VehicleOwnerDetails).filter(
        VehicleOwnerDetails.vehicle_owner_id == vehicle_owner_id
    ).first()
    
    if not vehicle_owner_details:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vehicle owner details not found"
        )
    
    try:
        vehicle_owner_details.aadhar_status = document_status
        db.commit()
        db.refresh(vehicle_owner_details)
        return vehicle_owner_details
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update vehicle owner document status: {str(e)}"
        )

def get_vehicle_owner_cars(db: Session, vehicle_owner_id: str) -> List[CarDetails]:
    """Get all cars for a vehicle owner"""
    return db.query(CarDetails).filter(
        CarDetails.vehicle_owner_id == vehicle_owner_id
    ).all()

def get_vehicle_owner_drivers(db: Session, vehicle_owner_id: str) -> List[CarDriver]:
    """Get all drivers for a vehicle owner"""
    return db.query(CarDriver).filter(
        CarDriver.vehicle_owner_id == vehicle_owner_id
    ).all()

# ============ CAR MANAGEMENT ============

def update_car_account_status(db: Session, car_id: str, car_status: str) -> CarDetails:
    """Update car account status"""
    car = db.query(CarDetails).filter(
        CarDetails.id == car_id
    ).first()
    
    if not car:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Car not found"
        )
    
    try:
        car.car_status = CarStatusEnum[car_status.upper()]
        db.commit()
        db.refresh(car)
        return car
    except (KeyError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid car status. Must be one of: {[e.name for e in CarStatusEnum]}"
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update car status: {str(e)}"
        )

def update_car_document_status(
    db: Session, 
    car_id: str, 
    document_type: str, 
    document_status: DocumentStatusEnum
) -> CarDetails:
    """Update car document status"""
    car = db.query(CarDetails).filter(
        CarDetails.id == car_id
    ).first()
    
    if not car:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Car not found"
        )
    
    document_mapping = {
        "rc_front": ("rc_front_status",),
        "rc_back": ("rc_back_status",),
        "insurance": ("insurance_status",),
        "fc": ("fc_status",),
        "car_img": ("car_img_status",),
    }
    
    if document_type not in document_mapping:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid document type. Must be one of: {list(document_mapping.keys())}"
        )
    
    try:
        status_field = document_mapping[document_type][0]
        setattr(car, status_field, document_status)
        db.commit()
        db.refresh(car)
        return car
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update car document status: {str(e)}"
        )

# ============ DRIVER MANAGEMENT ============

def update_driver_account_status(db: Session, driver_id: str, driver_status: str) -> CarDriver:
    """Update driver account status"""
    driver = db.query(CarDriver).filter(
        CarDriver.id == driver_id
    ).first()
    
    if not driver:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Driver not found"
        )
    
    try:
        driver.driver_status = DriverStatusEnum[driver_status.upper()]
        db.commit()
        db.refresh(driver)
        return driver
    except (KeyError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid driver status. Must be one of: {[e.name for e in DriverStatusEnum]}"
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update driver status: {str(e)}"
        )

def update_driver_document_status(db: Session, driver_id: str, document_status: DocumentStatusEnum) -> CarDriver:
    """Update driver document status"""
    driver = db.query(CarDriver).filter(
        CarDriver.id == driver_id
    ).first()
    
    if not driver:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Driver not found"
        )
    
    try:
        driver.licence_front_status = document_status
        db.commit()
        db.refresh(driver)
        return driver
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update driver document status: {str(e)}"
        )

# ============ UNIFIED ACCOUNT MANAGEMENT ============

def get_all_accounts_unified(
    db: Session, 
    skip: int = 0, 
    limit: int = 100,
    account_type: Optional[str] = None,
    status_filter: Optional[str] = None
) -> Tuple[List[dict], int, int, int]:
    """
    Get all accounts (vendors, vehicle owners, drivers) in a unified format.
    
    Args:
        db: Database session
        skip: Number of records to skip
        limit: Maximum number of records to return
        account_type: Filter by account type ("vendor", "vehicle_owner", "driver", "quickdriver")
        status_filter: Filter by status ("active", "inactive", "pending", etc.)
    
    Returns:
        Tuple of (accounts list, total_count, active_count, inactive_count)
    """
    accounts = []
    
    # Get vendors
    if not account_type or account_type.lower() in ["vendor", "vendors"]:
        vendors_query = db.query(VendorDetails).join(VendorCredentials, VendorDetails.vendor_id == VendorCredentials.id)
        
        if status_filter:
            status_filter_upper = status_filter.upper()
            if status_filter_upper in ["ACTIVE", "INACTIVE", "PENDING"]:
                vendors_query = vendors_query.filter(VendorCredentials.account_status == VendorAccountStatusEnum[status_filter_upper])
            elif status_filter.lower() in ["active", "inactive"]:
                # Handle active/inactive filter
                if status_filter.lower() == "active":
                    vendors_query = vendors_query.filter(VendorCredentials.account_status == VendorAccountStatusEnum.ACTIVE)
                else:
                    vendors_query = vendors_query.filter(VendorCredentials.account_status == VendorAccountStatusEnum.INACTIVE)
        
        # Get all vendors first (we'll paginate later after combining all account types)
        vendors = vendors_query.all()
        
        for vendor in vendors:
            vendor_cred = db.query(VendorCredentials).filter(VendorCredentials.id == vendor.vendor_id).first()
            accounts.append({
                "id": vendor.vendor_id,
                "name": vendor.full_name,
                "account_type": "vendor",
                "account_status": vendor_cred.account_status.value if vendor_cred else "Pending"
            })
    
    # Get vehicle owners
    if not account_type or account_type.lower() in ["vehicle_owner", "vehicle_owners", "vehicleowner"]:
        owners_query = db.query(VehicleOwnerDetails).join(VehicleOwnerCredentials, VehicleOwnerDetails.vehicle_owner_id == VehicleOwnerCredentials.id)
        
        if status_filter:
            status_filter_upper = status_filter.upper()
            if status_filter_upper in ["ACTIVE", "INACTIVE", "PENDING"]:
                owners_query = owners_query.filter(VehicleOwnerCredentials.account_status == VehicleOwnerAccountStatusEnum[status_filter_upper])
            elif status_filter.lower() in ["active", "inactive"]:
                # Handle active/inactive filter
                if status_filter.lower() == "active":
                    owners_query = owners_query.filter(VehicleOwnerCredentials.account_status == VehicleOwnerAccountStatusEnum.ACTIVE)
                else:
                    owners_query = owners_query.filter(VehicleOwnerCredentials.account_status == VehicleOwnerAccountStatusEnum.INACTIVE)
        
        # Get all owners first
        owners = owners_query.all()
        
        for owner in owners:
            owner_cred = db.query(VehicleOwnerCredentials).filter(VehicleOwnerCredentials.id == owner.vehicle_owner_id).first()
            accounts.append({
                "id": owner.vehicle_owner_id,
                "name": owner.full_name,
                "account_type": "vehicle_owner",
                "account_status": owner_cred.account_status.value if owner_cred else "Inactive"
            })
    
    # Get drivers (including quickdriver as same type)
    if not account_type or account_type.lower() in ["driver", "drivers", "quickdriver", "quickdrivers"]:
        drivers_query = db.query(CarDriver)
        
        if status_filter:
            status_filter_upper = status_filter.upper()
            if status_filter_upper in ["ONLINE", "OFFLINE", "DRIVING", "BLOCKED", "PROCESSING"]:
                try:
                    drivers_query = drivers_query.filter(CarDriver.driver_status == DriverStatusEnum[status_filter_upper])
                except KeyError:
                    pass
            elif status_filter.lower() in ["active", "inactive"]:
                # Handle active/inactive filter for drivers
                if status_filter.lower() == "active":
                    drivers_query = drivers_query.filter(CarDriver.driver_status.in_([DriverStatusEnum.ONLINE, DriverStatusEnum.DRIVING]))
                else:
                    drivers_query = drivers_query.filter(CarDriver.driver_status.in_([DriverStatusEnum.OFFLINE, DriverStatusEnum.BLOCKED, DriverStatusEnum.PROCESSING]))
        
        # Get all drivers first
        drivers = drivers_query.all()
        
        for driver in drivers:
            accounts.append({
                "id": driver.id,
                "name": driver.full_name,
                "account_type": "driver",  # Treat quickdriver same as driver
                "account_status": driver.driver_status.value
            })
    
    # Calculate counts before pagination
    total_count = len(accounts)
    active_count = sum(1 for acc in accounts if (
        (acc["account_type"] in ["vendor", "vehicle_owner"] and acc["account_status"].lower() == "active") or
        (acc["account_type"] == "driver" and acc["account_status"].upper() in ["ONLINE", "DRIVING"])
    ))
    inactive_count = total_count - active_count
    
    # Apply pagination after combining all accounts
    paginated_accounts = accounts[skip:skip + limit] if skip > 0 or limit < total_count else accounts
    
    return paginated_accounts, total_count, active_count, inactive_count

def get_account_details_by_id(db: Session, account_id: str, account_type: str) -> Optional[dict]:
    """
    Get full account details by ID and type.
    
    Args:
        db: Database session
        account_id: Account ID (UUID string)
        account_type: Account type ("vendor", "vehicle_owner", "driver", "quickdriver")
    
    Returns:
        Dictionary with full account details or None if not found
    """
    account_type_lower = account_type.lower()
    
    if account_type_lower in ["vendor", "vendors"]:
        vendor_cred = db.query(VendorCredentials).filter(VendorCredentials.id == account_id).first()
        if not vendor_cred:
            return None
        
        vendor_details = db.query(VendorDetails).filter(VendorDetails.vendor_id == account_id).first()
        if not vendor_details:
            return None
        
        return {
            "id": vendor_cred.id,
            "account_type": "vendor",
            "account_status": vendor_cred.account_status.value,
            "vendor_id": vendor_details.vendor_id,
            "full_name": vendor_details.full_name,
            "primary_number": vendor_details.primary_number,
            "secondary_number": vendor_details.secondary_number,
            "gpay_number": vendor_details.gpay_number,
            "wallet_balance": vendor_details.wallet_balance,
            "bank_balance": vendor_details.bank_balance,
            "aadhar_number": vendor_details.aadhar_number,
            "aadhar_front_img": vendor_details.aadhar_front_img,
            "aadhar_status": vendor_details.aadhar_status.value if vendor_details.aadhar_status else None,
            "address": vendor_details.address,
            "city": vendor_details.city,
            "pincode": vendor_details.pincode,
            "created_at": vendor_details.created_at
        }
    
    elif account_type_lower in ["vehicle_owner", "vehicle_owners", "vehicleowner"]:
        owner_cred = db.query(VehicleOwnerCredentials).filter(VehicleOwnerCredentials.id == account_id).first()
        if not owner_cred:
            return None
        
        owner_details = db.query(VehicleOwnerDetails).filter(VehicleOwnerDetails.vehicle_owner_id == account_id).first()
        if not owner_details:
            return None
        
        return {
            "id": owner_cred.id,
            "account_type": "vehicle_owner",
            "account_status": owner_cred.account_status.value,
            "vehicle_owner_id": owner_details.vehicle_owner_id,
            "full_name": owner_details.full_name,
            "primary_number": owner_details.primary_number,
            "secondary_number": owner_details.secondary_number,
            "wallet_balance": owner_details.wallet_balance,
            "aadhar_number": owner_details.aadhar_number,
            "aadhar_front_img": owner_details.aadhar_front_img,
            "aadhar_status": owner_details.aadhar_status.value if owner_details.aadhar_status else None,
            "address": owner_details.address,
            "city": owner_details.city,
            "pincode": owner_details.pincode,
            "created_at": owner_details.created_at
        }
    
    elif account_type_lower in ["driver", "drivers", "quickdriver", "quickdrivers"]:
        driver = db.query(CarDriver).filter(CarDriver.id == account_id).first()
        if not driver:
            return None
        
        return {
            "id": driver.id,
            "account_type": "driver",
            "account_status": driver.driver_status.value,
            "vehicle_owner_id": driver.vehicle_owner_id,
            "full_name": driver.full_name,
            "primary_number": driver.primary_number,
            "secondary_number": driver.secondary_number,
            "licence_number": driver.licence_number,
            "licence_front_img": driver.licence_front_img,
            "licence_front_status": driver.licence_front_status.value if driver.licence_front_status else None,
            "address": driver.address,
            "city": driver.city,
            "pincode": driver.pincode,
            "created_at": driver.created_at
        }
    
    return None

# ============ DOCUMENT VERIFICATION MANAGEMENT ============

def get_all_account_documents(db: Session, account_id: str, account_type: str) -> Optional[dict]:
    """
    Get all documents for an account (account documents + car documents if vehicle owner).
    
    Args:
        db: Database session
        account_id: Account ID (UUID string)
        account_type: Account type ("vendor", "vehicle_owner", "driver", "quickdriver")
    
    Returns:
        Dictionary with all documents organized by type
    """
    from app.utils.gcs import generate_signed_url_from_gcs
    
    account_type_lower = account_type.lower()
    account_documents = []
    car_documents = []
    
    if account_type_lower in ["vendor", "vendors"]:
        vendor_details = db.query(VendorDetails).filter(VendorDetails.vendor_id == account_id).first()
        if vendor_details and vendor_details.aadhar_front_img:
            account_documents.append({
                "document_id": "account_aadhar",
                "document_type": "aadhar",
                "document_name": "Aadhar Card",
                "image_url": generate_signed_url_from_gcs(vendor_details.aadhar_front_img) if vendor_details.aadhar_front_img else None,
                "status": vendor_details.aadhar_status.value if vendor_details.aadhar_status else "PENDING",
                "uploaded_at": vendor_details.created_at,
                "car_id": None,
                "car_name": None,
                "car_number": None
            })
    
    elif account_type_lower in ["vehicle_owner", "vehicle_owners", "vehicleowner"]:
        owner_details = db.query(VehicleOwnerDetails).filter(VehicleOwnerDetails.vehicle_owner_id == account_id).first()
        if owner_details:
            # Account document (Aadhar)
            if owner_details.aadhar_front_img:
                account_documents.append({
                    "document_id": "account_aadhar",
                    "document_type": "aadhar",
                    "document_name": "Aadhar Card",
                    "image_url": generate_signed_url_from_gcs(owner_details.aadhar_front_img) if owner_details.aadhar_front_img else None,
                    "status": owner_details.aadhar_status.value if owner_details.aadhar_status else "PENDING",
                    "uploaded_at": owner_details.created_at,
                    "car_id": None,
                    "car_name": None,
                    "car_number": None
                })
            
            # Get all cars and their documents
            cars = db.query(CarDetails).filter(CarDetails.vehicle_owner_id == account_id).all()
            for car in cars:
                car_doc_types = [
                    ("rc_front", "RC Front", car.rc_front_img_url, car.rc_front_status),
                    ("rc_back", "RC Back", car.rc_back_img_url, car.rc_back_status),
                    ("insurance", "Insurance", car.insurance_img_url, car.insurance_status),
                    ("fc", "Fitness Certificate", car.fc_img_url, car.fc_status),
                    ("car_img", "Car Image", car.car_img_url, car.car_img_status),
                    ("permit", "Permit", car.permit_img_url, car.permit_status),
                ]
                
                for doc_type, doc_name, img_url, doc_status in car_doc_types:
                    if img_url:
                        car_documents.append({
                            "document_id": f"car_{car.id}_{doc_type}",
                            "document_type": doc_type,
                            "document_name": f"{doc_name} - {car.car_name}",
                            "image_url": generate_signed_url_from_gcs(img_url) if img_url else None,
                            "status": doc_status.value if doc_status else "PENDING",
                            "uploaded_at": car.created_at,
                            "car_id": car.id,
                            "car_name": car.car_name,
                            "car_number": car.car_number
                        })
    
    elif account_type_lower in ["driver", "drivers", "quickdriver", "quickdrivers"]:
        driver = db.query(CarDriver).filter(CarDriver.id == account_id).first()
        if driver and driver.licence_front_img:
            account_documents.append({
                "document_id": "account_licence",
                "document_type": "licence",
                "document_name": "Driving License",
                "image_url": generate_signed_url_from_gcs(driver.licence_front_img) if driver.licence_front_img else None,
                "status": driver.licence_front_status.value if driver.licence_front_status else "PENDING",
                "uploaded_at": driver.created_at,
                "car_id": None,
                "car_name": None,
                "car_number": None
            })
    
    # Calculate counts
    all_docs = account_documents + car_documents
    pending_count = sum(1 for doc in all_docs if doc["status"] == "PENDING")
    verified_count = sum(1 for doc in all_docs if doc["status"] == "VERIFIED")
    invalid_count = sum(1 for doc in all_docs if doc["status"] == "INVALID")
    
    # Get account name
    account_name = ""
    if account_type_lower in ["vendor", "vendors"]:
        vendor_details = db.query(VendorDetails).filter(VendorDetails.vendor_id == account_id).first()
        account_name = vendor_details.full_name if vendor_details else ""
    elif account_type_lower in ["vehicle_owner", "vehicle_owners", "vehicleowner"]:
        owner_details = db.query(VehicleOwnerDetails).filter(VehicleOwnerDetails.vehicle_owner_id == account_id).first()
        account_name = owner_details.full_name if owner_details else ""
    elif account_type_lower in ["driver", "drivers", "quickdriver", "quickdrivers"]:
        driver = db.query(CarDriver).filter(CarDriver.id == account_id).first()
        account_name = driver.full_name if driver else ""
    
    return {
        "account_id": account_id,
        "account_type": account_type_lower.replace("s", "").replace("owner", "_owner"),
        "account_name": account_name,
        "account_documents": account_documents,
        "car_documents": car_documents,
        "total_documents": len(all_docs),
        "pending_count": pending_count,
        "verified_count": verified_count,
        "invalid_count": invalid_count
    }

def update_document_status_by_id(db: Session, account_id: str, account_type: str, document_id: str, new_status: str) -> dict:
    """
    Update document status by document_id.
    
    Document ID format:
    - Account documents: "account_aadhar", "account_licence"
    - Car documents: "car_{car_id}_{doc_type}" (e.g., "car_123_rc_front")
    
    Args:
        db: Database session
        account_id: Account ID (for account documents)
        account_type: Account type (for account documents)
        document_id: Document identifier
        new_status: New status ("PENDING", "VERIFIED", "INVALID")
    
    Returns:
        Dictionary with update result
    """
    try:
        doc_status = DocumentStatusEnum[new_status.upper()]
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid document status. Must be one of: PENDING, VERIFIED, INVALID"
        )
    
    # Parse document_id
    if document_id.startswith("account_"):
        # Account document - use account_id and account_type
        doc_type = document_id.replace("account_", "")
        return update_account_document_status(db, account_id, account_type, doc_type, new_status)
    
    elif document_id.startswith("car_"):
        # Car document: format is "car_{car_id}_{doc_type}"
        parts = document_id.split("_")
        if len(parts) < 3:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid car document ID format. Expected: car_{car_id}_{doc_type}"
            )
        
        car_id = parts[1]
        doc_type = "_".join(parts[2:])  # Handle doc types like "car_img"
        
        car = db.query(CarDetails).filter(CarDetails.id == car_id).first()
        if not car:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Car not found with ID {car_id}"
            )
        
        # Map document type to status field
        status_field_map = {
            "rc_front": "rc_front_status",
            "rc_back": "rc_back_status",
            "insurance": "insurance_status",
            "fc": "fc_status",
            "car_img": "car_img_status",
            "permit": "permit_status",
        }
        
        if doc_type not in status_field_map:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid document type. Must be one of: {list(status_field_map.keys())}"
            )
        
        setattr(car, status_field_map[doc_type], doc_status)
        db.commit()
        db.refresh(car)
        
        return {
            "message": f"Car {doc_type} document status updated successfully",
            "document_id": document_id,
            "document_type": doc_type,
            "new_status": new_status.upper()
        }
    
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Invalid document ID format"
    )

def update_account_document_status(db: Session, account_id: str, account_type: str, document_type: str, new_status: str) -> dict:
    """
    Update account document status (aadhar or licence).
    
    Args:
        db: Database session
        account_id: Account ID
        account_type: Account type
        document_type: "aadhar" or "licence"
        new_status: New status
    
    Returns:
        Dictionary with update result
    """
    try:
        doc_status = DocumentStatusEnum[new_status.upper()]
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid document status. Must be one of: PENDING, VERIFIED, INVALID"
        )
    
    account_type_lower = account_type.lower()
    
    if account_type_lower in ["vendor", "vendors"]:
        if document_type != "aadhar":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Vendors only have Aadhar documents"
            )
        vendor_details = db.query(VendorDetails).filter(VendorDetails.vendor_id == account_id).first()
        if not vendor_details:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Vendor not found"
            )
        vendor_details.aadhar_status = doc_status
        db.commit()
        db.refresh(vendor_details)
        return {
            "message": "Vendor Aadhar document status updated successfully",
            "document_id": f"account_{document_type}",
            "document_type": document_type,
            "new_status": new_status.upper()
        }
    
    elif account_type_lower in ["vehicle_owner", "vehicle_owners", "vehicleowner"]:
        if document_type != "aadhar":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Vehicle owners only have Aadhar documents"
            )
        owner_details = db.query(VehicleOwnerDetails).filter(VehicleOwnerDetails.vehicle_owner_id == account_id).first()
        if not owner_details:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Vehicle owner not found"
            )
        owner_details.aadhar_status = doc_status
        db.commit()
        db.refresh(owner_details)
        return {
            "message": "Vehicle Owner Aadhar document status updated successfully",
            "document_id": f"account_{document_type}",
            "document_type": document_type,
            "new_status": new_status.upper()
        }
    
    elif account_type_lower in ["driver", "drivers", "quickdriver", "quickdrivers"]:
        if document_type != "licence":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Drivers only have License documents"
            )
        driver = db.query(CarDriver).filter(CarDriver.id == account_id).first()
        if not driver:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Driver not found"
            )
        driver.licence_front_status = doc_status
        db.commit()
        db.refresh(driver)
        return {
            "message": "Driver License document status updated successfully",
            "document_id": f"account_{document_type}",
            "document_type": document_type,
            "new_status": new_status.upper()
        }
    
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Invalid account type"
    )