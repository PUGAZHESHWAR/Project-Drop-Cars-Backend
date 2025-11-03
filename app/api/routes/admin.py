# api/routes/admin.py
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.schemas.admin import AdminSignup, AdminSignin, AdminTokenResponse, AdminOut, AdminUpdate
from app.schemas.admin_add_money import VehicleOwnerInfoResponse, SearchVehicleOwnerRequest, AdminAddMoneyRequest, AdminAddMoneyResponse
from app.crud.admin import create_admin, authenticate_admin, get_admin_by_id, update_admin, get_all_admins
from app.crud.admin_add_money import get_vehicle_owner_by_primary_number, create_admin_add_money_transaction
from app.core.security import create_access_token, get_current_admin
from app.database.session import get_db
from app.utils.gcs import upload_image_to_gcs
from typing import List, Optional
from uuid import UUID
from datetime import datetime
import os

router = APIRouter()

@router.post("/admin/signup", response_model=AdminTokenResponse, status_code=status.HTTP_201_CREATED)
async def admin_signup(
    admin_data: AdminSignup,
    db: Session = Depends(get_db)
):
    """
    Admin Signup API
    
    Creates a new admin account with credentials.
    Returns JWT access token for authentication.
    
    Returns:
        - Access token for authentication
        - Admin details
    """
    try:
        # Check if admin already exists with the same username
        from app.crud.admin import get_admin_by_username
        existing_admin = get_admin_by_username(db, admin_data.username)
        if existing_admin:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Admin with this username already registered"
            )
        
        # Check if admin already exists with the same email
        from app.crud.admin import get_admin_by_email
        existing_email = get_admin_by_email(db, admin_data.email)
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Admin with this email already registered"
            )
        
        # Check if admin already exists with the same phone
        from app.crud.admin import get_admin_by_phone
        existing_phone = get_admin_by_phone(db, admin_data.phone)
        if existing_phone:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Admin with this phone number already registered"
            )
        
        # Hash password and create admin
        from app.core.security import get_password_hash
        hashed_password = get_password_hash(admin_data.password)
        
        admin = create_admin(
            db=db,
            username=admin_data.username,
            hashed_password=hashed_password,
            role=admin_data.role,
            email=admin_data.email,
            phone=admin_data.phone
        )
        
        # Create access token
        access_token = create_access_token({"sub": str(admin.id)})
        
        # Prepare response
        admin_response = AdminOut(
            id=admin.id,
            username=admin.username,
            email=admin.email,
            phone=admin.phone,
            role=admin.role,
            organization_id=admin.organization_id,
            created_at=admin.created_at
        )
        
        return AdminTokenResponse(
            access_token=access_token,
            token_type="bearer",
            admin=admin_response
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )

@router.post("/admin/signin", response_model=AdminTokenResponse)
async def admin_signin(
    admin_data: AdminSignin,
    db: Session = Depends(get_db)
):
    """
    Admin Signin API
    
    Authenticates admin with username and password.
    Returns JWT access token upon successful authentication.
    
    Returns:
        - Access token for authentication
        - Admin details
    """
    try:
        # Authenticate admin
        admin = authenticate_admin(db, admin_data.username, admin_data.password)
        
        if not admin:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password"
            )
        
        # Create access token
        access_token = create_access_token({"sub": str(admin.id)})
        
        # Prepare response
        admin_response = AdminOut(
            id=admin.id,
            username=admin.username,
            email=admin.email,
            phone=admin.phone,
            role=admin.role,
            organization_id=admin.organization_id,
            created_at=admin.created_at
        )
        
        return AdminTokenResponse(
            access_token=access_token,
            token_type="bearer",
            admin=admin_response
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )

@router.get("/admin/profile", response_model=AdminOut)
async def get_admin_profile(
    current_admin = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    Get current admin profile
    
    Returns the profile of the currently authenticated admin.
    
    Returns:
        - Admin profile details
    """
    try:
        return current_admin
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )

@router.put("/admin/profile", response_model=AdminOut)
async def update_admin_profile(
    admin_update: AdminUpdate,
    current_admin = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    Update admin profile
    
    Allows admin to update their profile information.
    
    Returns:
        - Updated admin profile details
    """
    try:
        # Update admin profile
        updated_admin = update_admin(db, str(current_admin.id), **admin_update.dict(exclude_unset=True))
        
        return updated_admin
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )

@router.get("/admin/list", response_model=List[AdminOut])
async def list_admins(
    skip: int = 0,
    limit: int = 100,
    current_admin = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    List all admins (Admin only)
    
    Returns a list of all admin accounts in the system.
    Requires admin authentication.
    
    Returns:
        - List of admin accounts
    """
    try:
        # Check if current admin has permission to list all admins
        if current_admin.role not in ["Owner", "Manager"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions to list all admins"
            )
        
        admins, total_count = get_all_admins(db, skip, limit)
        
        return admins
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )

@router.get("/admin/{admin_id}", response_model=AdminOut)
async def get_admin_by_id_route(
    admin_id: str,
    current_admin = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    Get admin by ID (Admin only)
    
    Returns details of a specific admin account.
    Requires admin authentication.
    
    Returns:
        - Admin account details
    """
    try:
        # Check if current admin has permission
        if current_admin.role not in ["Owner", "Manager"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions to view admin details"
            )
        
        admin = get_admin_by_id(db, admin_id)
        if not admin:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Admin not found"
            )
        
        return admin
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


# === Admin: Orders Management ===

@router.get("/admin/orders")
async def admin_list_orders(
    vendor_id: Optional[str] = None,
    trip_status: Optional[str] = None,
    source: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    current_admin = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    from app.models.orders import Order, OrderSourceEnum
    query = db.query(Order)
    if vendor_id:
        query = query.filter(Order.vendor_id == vendor_id)
    if trip_status:
        query = query.filter(Order.trip_status == trip_status)
    if source:
        try:
            query = query.filter(Order.source == OrderSourceEnum(source))
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid source")
    if start_date:
        try:
            dt = datetime.fromisoformat(start_date)
            query = query.filter(Order.created_at >= dt)
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid start_date (use ISO format)")
    if end_date:
        try:
            dt = datetime.fromisoformat(end_date)
            query = query.filter(Order.created_at <= dt)
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid end_date (use ISO format)")
    return query.order_by(Order.created_at.desc()).all()


@router.patch("/admin/orders/{order_id}/cancel")
async def admin_cancel_order(
    order_id: int,
    reason: Optional[str] = Form(None),
    current_admin = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    from app.models.orders import Order
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    order.trip_status = "CANCELLED"
    order.cancelled_by = "ADMIN"
    db.commit()
    db.refresh(order)
    return {"order_id": order.id, "trip_status": order.trip_status, "cancelled_by": order.cancelled_by, "reason": reason}


# === Admin: Drivers Management ===

@router.get("/admin/drivers")
async def admin_list_drivers(
    vehicle_owner_id: Optional[str] = None,
    status_filter: Optional[str] = None,
    current_admin = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    from app.models.car_driver import CarDriver, AccountStatusEnum
    query = db.query(CarDriver)
    if vehicle_owner_id:
        query = query.filter(CarDriver.vehicle_owner_id == vehicle_owner_id)
    if status_filter:
        try:
            query = query.filter(CarDriver.driver_status == AccountStatusEnum(status_filter))
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid status_filter")
    return query.order_by(CarDriver.created_at.desc()).all()


@router.patch("/admin/drivers/{driver_id}/status")
async def admin_update_driver_status(
    driver_id: str,
    new_status: str = Form(...),
    current_admin = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    from app.models.car_driver import CarDriver, AccountStatusEnum
    driver = db.query(CarDriver).filter(CarDriver.id == driver_id).first()
    if not driver:
        raise HTTPException(status_code=404, detail="Driver not found")
    try:
        driver.driver_status = AccountStatusEnum(new_status)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid new_status")
    db.commit()
    db.refresh(driver)
    return {"driver_id": str(driver.id), "new_status": driver.driver_status}


@router.patch("/admin/drivers/{driver_id}/document-status")
async def admin_update_driver_document_status(
    driver_id: str,
    status_value: str = Form(...),
    current_admin = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    from app.models.car_driver import CarDriver
    from app.models.common_enums import DocumentStatusEnum
    driver = db.query(CarDriver).filter(CarDriver.id == driver_id).first()
    if not driver:
        raise HTTPException(status_code=404, detail="Driver not found")
    try:
        driver.licence_front_status = DocumentStatusEnum(status_value)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid document status")
    db.commit()
    db.refresh(driver)
    return {"driver_id": str(driver.id), "licence_status": driver.licence_front_status}


# === Admin: Vehicle Owners Management ===

@router.get("/admin/vehicle-owners")
async def admin_list_vehicle_owners(
    mobile: Optional[str] = None,
    city: Optional[str] = None,
    current_admin = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    from app.models.vehicle_owner_details import VehicleOwnerDetails
    query = db.query(VehicleOwnerDetails)
    if mobile:
        query = query.filter(VehicleOwnerDetails.primary_number == mobile)
    if city:
        query = query.filter(VehicleOwnerDetails.city == city)
    return query.order_by(VehicleOwnerDetails.created_at.desc()).all()


@router.patch("/admin/vehicle-owners/{owner_id}/document-status")
async def admin_update_owner_document_status(
    owner_id: str,
    status_value: str = Form(...),
    current_admin = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    from app.models.vehicle_owner_details import VehicleOwnerDetails
    from app.models.common_enums import DocumentStatusEnum
    details = db.query(VehicleOwnerDetails).filter(VehicleOwnerDetails.vehicle_owner_id == owner_id).first()
    if not details:
        raise HTTPException(status_code=404, detail="Vehicle owner not found")
    try:
        details.aadhar_status = DocumentStatusEnum(status_value)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid document status")
    db.commit()
    db.refresh(details)
    return {"vehicle_owner_id": str(details.vehicle_owner_id), "aadhar_status": details.aadhar_status}


# === Admin: Vendors Management ===

@router.get("/admin/vendors")
async def admin_list_vendors(
    mobile: Optional[str] = None,
    city: Optional[str] = None,
    current_admin = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    from app.models.vendor_details import VendorDetails
    query = db.query(VendorDetails)
    if mobile:
        query = query.filter(VendorDetails.primary_number == mobile)
    if city:
        query = query.filter(VendorDetails.city == city)
    return query.order_by(VendorDetails.created_at.desc()).all()


@router.patch("/admin/vendors/{vendor_id}/document-status")
async def admin_update_vendor_document_status(
    vendor_id: str,
    status_value: str = Form(...),
    current_admin = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    from app.models.vendor_details import VendorDetails
    from app.models.common_enums import DocumentStatusEnum
    details = db.query(VendorDetails).filter(VendorDetails.vendor_id == vendor_id).first()
    if not details:
        raise HTTPException(status_code=404, detail="Vendor not found")
    try:
        details.aadhar_status = DocumentStatusEnum(status_value)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid document status")
    db.commit()
    db.refresh(details)
    return {"vendor_id": str(details.vendor_id), "aadhar_status": details.aadhar_status}


# === Admin: Wallets & Transactions Views ===

@router.get("/admin/vehicle-owners/{owner_id}/wallet/ledger")
async def admin_owner_wallet_ledger(
    owner_id: str,
    current_admin = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    from app.models.wallet_ledger import WalletLedger
    return db.query(WalletLedger).filter(WalletLedger.vehicle_owner_id == owner_id).order_by(WalletLedger.created_at.desc()).all()


@router.get("/admin/vendors/{vendor_id}/wallet/ledger")
async def admin_vendor_wallet_ledger(
    vendor_id: str,
    current_admin = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    from app.models.vendor_wallet_ledger import VendorWalletLedger
    return db.query(VendorWalletLedger).filter(VendorWalletLedger.vendor_id == vendor_id).order_by(VendorWalletLedger.created_at.desc()).all()


@router.get("/admin/admin-wallet/ledger")
async def admin_wallet_ledger(
    current_admin = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    from app.models.admin_wallet_ledger import AdminWalletLedger
    return db.query(AdminWalletLedger).filter(AdminWalletLedger.admin_id == current_admin.id).order_by(AdminWalletLedger.created_at.desc()).all()


@router.get("/admin/admin-wallet/balance")
async def get_admin_wallet_balance(
    current_admin = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    from app.crud.admin_wallet import get_admin_balance
    balance = get_admin_balance(db, str(current_admin.id))
    return {"admin_id": str(current_admin.id), "current_balance": balance}


@router.get("/admin/razorpay-transactions")
async def admin_list_razorpay_transactions(
    status_filter: Optional[str] = None,
    owner_id: Optional[str] = None,
    current_admin = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    from app.models.razorpay_transactions import RazorpayTransaction, RazorpayPaymentStatusEnum
    query = db.query(RazorpayTransaction)
    if owner_id:
        query = query.filter(RazorpayTransaction.vehicle_owner_id == owner_id)
    if status_filter:
        try:
            query = query.filter(RazorpayTransaction.status == RazorpayPaymentStatusEnum(status_filter))
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid status_filter")
    return query.order_by(RazorpayTransaction.created_at.desc()).all()

@router.post("/admin/search-vehicle-owner", response_model=VehicleOwnerInfoResponse, status_code=status.HTTP_200_OK)
async def search_vehicle_owner(
    search_request: SearchVehicleOwnerRequest,
    current_admin = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    Search Vehicle Owner by Primary Number
    
    Searches for a vehicle owner by their primary phone number.
    Returns vehicle owner information including wallet balance and profile details.
    
    Requires admin authentication.
    
    Returns:
        - Vehicle owner information
        - Wallet balance
        - Profile details
    """
    try:
        vehicle_owner_info = get_vehicle_owner_by_primary_number(db, search_request.primary_number)
        return VehicleOwnerInfoResponse(**vehicle_owner_info)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


@router.post("/admin/add-money-to-vehicle-owner", response_model=AdminAddMoneyResponse, status_code=status.HTTP_201_CREATED)
async def add_money_to_vehicle_owner(
    vehicle_owner_id: str = Form(..., description="ID of the vehicle owner"),
    transaction_value: int = Form(..., description="Transaction amount in paise (mandatory)"),
    notes: Optional[str] = Form(None, description="Transaction notes"),
    reference_value: Optional[str] = Form(None, description="Optional reference string for the transaction"),
    transaction_img: UploadFile = File(None),
    current_admin = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    Add Money to Vehicle Owner
    
    Creates a payment transaction to add money to a vehicle owner's wallet.
    
    Requires admin authentication.
    
    Steps:
    1. Validates vehicle owner exists
    2. Uploads transaction image to GCS if provided (optional)
    3. Updates vehicle owner's wallet balance
    4. Creates wallet ledger entry
    5. Records transaction in admin_add_money_to_vehicle_owner table
    
    Returns:
        - Transaction details
        - New wallet balance
        - Transaction ID
    """
    try:
        transaction_img_url = None
        
        # Upload transaction image to GCS if provided
        if transaction_img:
            # Validate file type
            allowed_extensions = {'.jpg', '.jpeg', '.png', '.pdf'}
            file_ext = os.path.splitext(transaction_img.filename)[-1].lower()
            if file_ext not in allowed_extensions:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid file type. Allowed types: {', '.join(allowed_extensions)}"
                )
            
            # Upload to GCS
            transaction_img_url = upload_image_to_gcs(
                transaction_img,
                folder="admin_transactions"
            )
        
        # Create transaction
        result = create_admin_add_money_transaction(
            db=db,
            vehicle_owner_id=vehicle_owner_id,
            transaction_value=transaction_value,
            transaction_img=transaction_img_url,
            notes=notes,
            reference_value=reference_value
        )
        
        return AdminAddMoneyResponse(**result)
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )
