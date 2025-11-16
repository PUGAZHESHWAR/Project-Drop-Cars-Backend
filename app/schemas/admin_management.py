# schemas/admin_management.py
from pydantic import BaseModel
from typing import Optional, List, Dict
from uuid import UUID
from datetime import datetime
from app.models.common_enums import DocumentStatusEnum

# ============ VENDOR SCHEMAS ============

class VendorListResponse(BaseModel):
    """Response schema for vendor list item"""
    id: UUID
    vendor_id: UUID
    full_name: str
    primary_number: str
    secondary_number: Optional[str]
    gpay_number: str
    wallet_balance: int
    bank_balance: int
    aadhar_number: str
    aadhar_front_img: Optional[str]
    address: str
    city: str
    pincode: str
    created_at: datetime

    class Config:
        from_attributes = True

class VendorListOut(BaseModel):
    """Response schema for vendor list with pagination"""
    vendors: List[VendorListResponse]
    total_count: int

class VendorDocumentInfo(BaseModel):
    """Vendor document information"""
    document_type: str
    status: Optional[str]
    image_url: Optional[str]

class VendorFullDetailsResponse(BaseModel):
    """Response schema for vendor full details"""
    id: UUID
    vendor_id: UUID
    full_name: str
    primary_number: str
    secondary_number: Optional[str]
    gpay_number: str
    wallet_balance: int
    bank_balance: int
    aadhar_number: str
    aadhar_front_img: Optional[str]
    aadhar_status: Optional[str]
    address: str
    city: str
    pincode: str
    account_status: str
    documents: Dict[str, VendorDocumentInfo]
    created_at: datetime

    class Config:
        from_attributes = True

class UpdateAccountStatusRequest(BaseModel):
    """Request schema for updating account status"""
    account_status: str

class UpdateDocumentStatusRequest(BaseModel):
    """Request schema for updating document status"""
    document_status: str

class StatusUpdateResponse(BaseModel):
    """Response schema for status update"""
    message: str
    id: UUID
    new_status: str

# ============ VEHICLE OWNER SCHEMAS ============

class VehicleOwnerListResponse(BaseModel):
    """Response schema for vehicle owner list item"""
    id: UUID
    vehicle_owner_id: UUID
    full_name: str
    primary_number: str
    secondary_number: Optional[str]
    wallet_balance: int
    aadhar_number: str
    aadhar_front_img: Optional[str]
    address: str
    city: str
    pincode: str
    created_at: datetime

    class Config:
        from_attributes = True

class VehicleOwnerListOut(BaseModel):
    """Response schema for vehicle owner list with pagination"""
    vehicle_owners: List[VehicleOwnerListResponse]
    total_count: int

class VehicleOwnerDocumentInfo(BaseModel):
    """Vehicle owner document information"""
    document_type: str
    status: Optional[str]
    image_url: Optional[str]

class VehicleOwnerFullDetailsResponse(BaseModel):
    """Response schema for vehicle owner full details"""
    id: UUID
    vehicle_owner_id: UUID
    full_name: str
    primary_number: str
    secondary_number: Optional[str]
    wallet_balance: int
    aadhar_number: str
    aadhar_front_img: Optional[str]
    aadhar_status: Optional[str]
    address: str
    city: str
    pincode: str
    account_status: str
    documents: Dict[str, VehicleOwnerDocumentInfo]
    created_at: datetime

    class Config:
        from_attributes = True

# ============ CAR SCHEMAS ============

class CarListItem(BaseModel):
    """Car list item schema"""
    id: UUID
    vehicle_owner_id: UUID
    car_name: str
    car_type: str
    car_number: str
    year_of_the_car: Optional[str]
    rc_front_img_url: Optional[str]
    rc_front_status: Optional[str]
    rc_back_img_url: Optional[str]
    rc_back_status: Optional[str]
    insurance_img_url: Optional[str]
    insurance_status: Optional[str]
    fc_img_url: Optional[str]
    fc_status: Optional[str]
    car_img_url: Optional[str]
    car_img_status: Optional[str]
    car_status: str
    created_at: datetime

    class Config:
        from_attributes = True

class CarListResponse(BaseModel):
    """Response schema for car list"""
    cars: List[CarListItem]

# ============ DRIVER SCHEMAS ============

class DriverListItem(BaseModel):
    """Driver list item schema"""
    id: UUID
    vehicle_owner_id: UUID
    full_name: str
    primary_number: str
    secondary_number: Optional[str]
    licence_number: str
    licence_front_img: Optional[str]
    licence_front_status: Optional[str]
    address: str
    city: str
    pincode: str
    driver_status: str
    created_at: datetime

    class Config:
        from_attributes = True

class DriverListResponse(BaseModel):
    """Response schema for driver list"""
    drivers: List[DriverListItem]

# ============ VEHICLE OWNER WITH CARS AND DRIVERS ============

class VehicleOwnerWithAssetsResponse(BaseModel):
    """Response schema for vehicle owner with cars and drivers"""
    vehicle_owner: VehicleOwnerFullDetailsResponse
    cars: List[CarListItem]
    drivers: List[DriverListItem]

# ============ UNIFIED ACCOUNT MANAGEMENT SCHEMAS ============

class AccountListItem(BaseModel):
    """Unified account list item with basic info"""
    id: UUID
    name: str
    account_type: str  # "vendor", "vehicle_owner", "driver", "quickdriver"
    account_status: str  # "Active", "Inactive", "Pending", "ONLINE", "OFFLINE", etc.
    
    class Config:
        from_attributes = True

class AccountListResponse(BaseModel):
    """Response schema for unified account list"""
    accounts: List[AccountListItem]
    total_count: int
    active_count: int
    inactive_count: int

class AccountFullDetailsResponse(BaseModel):
    """Unified response for full account details"""
    id: UUID
    account_type: str
    account_status: str
    # Vendor specific fields
    vendor_id: Optional[UUID] = None
    full_name: Optional[str] = None
    primary_number: Optional[str] = None
    secondary_number: Optional[str] = None
    gpay_number: Optional[str] = None
    wallet_balance: Optional[int] = None
    bank_balance: Optional[int] = None
    aadhar_number: Optional[str] = None
    aadhar_front_img: Optional[str] = None
    aadhar_status: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    pincode: Optional[str] = None
    # Vehicle Owner specific fields
    vehicle_owner_id: Optional[UUID] = None
    # Driver specific fields
    licence_number: Optional[str] = None
    licence_front_img: Optional[str] = None
    licence_front_status: Optional[str] = None
    # Common
    created_at: datetime
    documents: Optional[Dict[str, VendorDocumentInfo]] = None
    
    class Config:
        from_attributes = True

# ============ DOCUMENT VERIFICATION SCHEMAS ============

class DocumentItem(BaseModel):
    """Individual document item"""
    document_id: str  # Unique identifier: "account_aadhar", "car_1_rc_front", etc.
    document_type: str  # "aadhar", "licence", "rc_front", "rc_back", "insurance", "fc", "car_img", "permit"
    document_name: str  # Display name: "Aadhar Card", "RC Front", etc.
    image_url: Optional[str] = None
    status: str  # "PENDING", "VERIFIED", "INVALID"
    uploaded_at: Optional[datetime] = None
    # For car documents
    car_id: Optional[UUID] = None
    car_name: Optional[str] = None
    car_number: Optional[str] = None
    
    class Config:
        from_attributes = True

class AccountDocumentsResponse(BaseModel):
    """Response with all documents for an account"""
    account_id: UUID
    account_type: str
    account_name: str
    account_documents: List[DocumentItem]  # Account-level documents (aadhar/license)
    car_documents: List[DocumentItem] = []  # Car documents (if vehicle owner)
    total_documents: int
    pending_count: int
    verified_count: int
    invalid_count: int
    
    class Config:
        from_attributes = True

class UpdateDocumentStatusRequest(BaseModel):
    """Request to update a single document status"""
    document_id: str  # e.g., "account_aadhar", "car_1_rc_front"
    status: str  # "PENDING", "VERIFIED", "INVALID"
    
    class Config:
        json_schema_extra = {
            "example": {
                "document_id": "account_aadhar",
                "status": "VERIFIED"
            }
        }

class DocumentStatusUpdateResponse(BaseModel):
    """Response after updating document status"""
    message: str
    document_id: str
    document_type: str
    new_status: str
    
    class Config:
        from_attributes = True

# ============ CAR LIST SCHEMAS ============

class CarListItem(BaseModel):
    """Car list item with basic info"""
    id: UUID
    vehicle_owner_id: UUID
    car_name: str
    car_type: str
    car_number: str
    year_of_the_car: Optional[str] = None
    car_status: str  # ONLINE, DRIVING, BLOCKED, PROCESSING
    vehicle_owner_name: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

class CarListResponse(BaseModel):
    """Response schema for car list"""
    cars: List[CarListItem]
    total_count: int
    online_count: int
    blocked_count: int
    processing_count: int
    driving_count: int