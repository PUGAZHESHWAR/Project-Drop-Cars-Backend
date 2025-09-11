from pydantic import BaseModel, Field,field_validator
from typing import Any, List, Optional, Union, Literal, Dict
from uuid import UUID
from datetime import datetime
from enum import Enum


class OrderType(str,Enum):
    ONEWAY = "Oneway"
    ROUND_TRIP = "Round Trip"
    HOURLY_RENTAL = "Hourly Rental"
    MULTY_CITY = "Multy City"


class CarType(str,Enum):
    HATCHBACK = "Hatchback"
    SEDAN = "Sedan"
    NEW_SEDAN = "New Sedan"
    SUV = "SUV"
    INNOVA = "Innova"
    INNOVA_CRYSTA = "Innova Crysta"


class RentalOrderRequest(BaseModel):
    vendor_id: UUID
    trip_type: OrderType = Field(default=OrderType.HOURLY_RENTAL)
    car_type: CarType
    pickup_drop_location: Dict[str, str] = Field(
        description="Object mapping indices to location names, e.g. {\"0\": \"Chennai\", \"1\": \"Bangalore\"}"
    )
    start_date_time: datetime
    customer_name: str
    customer_number: str
    
    package_hours: int
    
    cost_per_pack: int
    extra_cost_per_pack: int
    additional_cost_per_hour: int
    extra_additional_cost_per_hour: int

    pickup_notes: Optional[str] = None

    @field_validator("pickup_drop_location")
    def validate_locations(cls, v: Dict[str, str]):
        if not isinstance(v, dict) or len(v.keys()) != 1:
            raise ValueError("pickup_drop_location must be an object with at one indices: source (0)")
        try:
            sorted([int(k) for k in v.keys()])
        except Exception:
            raise ValueError("pickup_drop_location keys must be numeric strings like '0', '1', ...")
        return v


class RentalFareBreakdown(BaseModel):
    total_hours: float
    vendor_amount: int
    vehicle_owner_amount: int


class HourlyQuoteResponse(BaseModel):
    fare: RentalFareBreakdown
    echo: RentalOrderRequest


class OrderSource(str, Enum):
    NEW_ORDERS = "NEW_ORDERS"
    HOURLY_RENTAL = "HOURLY_RENTAL"


class UnifiedOrder(BaseModel):
    id: int
    source: OrderSource
    source_order_id: int
    vendor_id: UUID
    trip_type: OrderType
    car_type: CarType
    pickup_drop_location: Dict[str, str]
    start_date_time: datetime
    customer_name: str
    customer_number: str
    trip_status: Optional[str] = None
    pick_near_city: Optional[str] = None
    trip_distance: Optional[int] = None
    trip_time: Optional[str] = None
    estimated_price: Optional[int] = None
    vendor_price: Optional[int] = None
    platform_fees_percent: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True


class CloseOrderRequest(BaseModel):
    closed_vendor_price: int
    closed_driver_price: int
    commision_amount: int
    start_km: int
    end_km: int
    contact_number: str

class CloseOrderResponse(BaseModel):
    order_id: int
    end_record_id: int
    img_url: str


class OnewayQuoteRequest(BaseModel):
    vendor_id: UUID
    trip_type: OrderType = Field(default=OrderType.ONEWAY)
    car_type: CarType
    pickup_drop_location: Dict[str, str] = Field(
        description="Object mapping indices to location names, e.g. {\"0\": \"Chennai\", \"1\": \"Bangalore\"}"
    )
    start_date_time: datetime
    customer_name: str
    customer_number: str
    cost_per_km: int
    extra_cost_per_km: int
    driver_allowance: int
    extra_driver_allowance: int
    permit_charges: int
    extra_permit_charges: int
    hill_charges: int
    toll_charges: int
    pickup_notes: Optional[str] = None

    @field_validator("pickup_drop_location")
    def validate_locations(cls, v: Dict[str, str]):
        if not isinstance(v, dict) or len(v.keys()) < 2:
            raise ValueError("pickup_drop_location must be an object with at least two indices: source (0) and destination (last)")
        # Ensure keys are numeric-like
        try:
            sorted([int(k) for k in v.keys()])
        except Exception:
            raise ValueError("pickup_drop_location keys must be numeric strings like '0', '1', ...")
        return v


class OnewayConfirmRequest(OnewayQuoteRequest):
    send_to: Literal["ALL", "NEAR_CITY"] = Field(
        description="Whether to send to all or only near city drivers"
    )
    near_city: Optional[str] = Field(
        default=None, description="City name when send_to is NEAR_CITY"
    )


class RoundTripQuoteRequest(OnewayQuoteRequest):
    trip_type: OrderType = Field(default=OrderType.ROUND_TRIP)


class RoundTripConfirmRequest(OnewayConfirmRequest):
    trip_type: OrderType = Field(default=OrderType.ROUND_TRIP)


class MulticityQuoteRequest(OnewayQuoteRequest):
    trip_type: OrderType = Field(default=OrderType.MULTY_CITY)


class MulticityConfirmRequest(OnewayConfirmRequest):
    trip_type: OrderType = Field(default=OrderType.MULTY_CITY)


class FareBreakdown(BaseModel):
    total_km: float
    trip_time: str
    base_km_amount: int
    driver_allowance: int
    extra_driver_allowance: int
    permit_charges: int
    hill_charges: int
    toll_charges: int
    total_amount: int


class OnewayQuoteResponse(BaseModel):
    fare: FareBreakdown
    echo: OnewayQuoteRequest


class OnewayConfirmResponse(BaseModel):
    order_id: int
    trip_status: str
    pick_near_city: str
    fare: FareBreakdown

class NewOrderResponse(BaseModel):
    order_id: int
    vendor_id: UUID
    trip_type: OrderType
    car_type: CarType
    pickup_drop_location: Dict[str, str]
    start_date_time: datetime
    customer_name: str
    customer_number: str
    cost_per_km: int
    extra_cost_per_km: int
    driver_allowance: int
    extra_driver_allowance: int
    permit_charges: int
    extra_permit_charges: int
    hill_charges: int
    toll_charges: int
    pickup_notes: Optional[str]
    trip_status: str
    pick_near_city: str
    trip_distance: int
    trip_time: str
    estimated_price: int
    vendor_price: int
    platform_fees_percent: int
    created_at: datetime

    class Config:
        from_attributes = True
