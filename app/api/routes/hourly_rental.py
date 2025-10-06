from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.core.security import get_current_vendor
from app.schemas.new_orders import (
    RentalOrderRequest,
    HourlyQuoteResponse,
    RentalFareBreakdown,
)
from app.crud.hourly_rental import calculate_hourly_fare, create_hourly_order
from app.crud.orders import create_master_from_hourly
from app.models.new_orders import OrderTypeEnum, CarTypeEnum
from pathlib import Path
import json
from fastapi.responses import JSONResponse


router = APIRouter()

JSON_FILE_PATH = Path("load_data\hourly_plans.json")
data_cache = {}


# Load JSON data once on startup
def load_data_once():
    global data_cache
    data_cache = load_json_file()
    print("Data loaded on startup")

def load_json_file():
    if JSON_FILE_PATH.exists():
        with open(JSON_FILE_PATH, "r") as f:
            return json.load(f)
    return {}

data_cache = load_json_file()

# GET /data — Serve cached data
@router.get("/rental_hrs_data")
def get_data():
    return JSONResponse(content=data_cache)

# POST /refresh — Reload data from JSON file
@router.post("/refresh-rental-hrs-data")
def refresh_data():
    global data_cache
    data_cache = load_json_file()
    return {"message": "Data refreshed", "data": data_cache}

@router.post("/hourly/quote", response_model=HourlyQuoteResponse)
async def hourly_quote(payload: RentalOrderRequest):
    try:
        fare = calculate_hourly_fare(
            payload.package_hours,
            payload.cost_per_hour,
            payload.extra_cost_per_hour,
            payload.cost_for_addon_km,
            payload.extra_cost_for_addon_km,
        )
        return HourlyQuoteResponse(
            fare=RentalFareBreakdown(**fare),
            echo=payload,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to calculate hourly fare: {str(e)}",
        )


@router.post("/hourly/confirm", status_code=status.HTTP_201_CREATED)
async def hourly_confirm(
    payload: RentalOrderRequest,
    db: Session = Depends(get_db),
    current_vendor=Depends(get_current_vendor),
):
    try:
        vendor_id = current_vendor.id

        order = create_hourly_order(
            db,
            vendor_id=vendor_id,
            trip_type=OrderTypeEnum.HOURLY_RENTAL,
            car_type=CarTypeEnum(payload.car_type),
            pickup_drop_location=payload.pickup_drop_location,
            start_date_time=payload.start_date_time,
            customer_name=payload.customer_name,
            customer_number=payload.customer_number,
            package_hours=payload.package_hours,
            cost_per_hour=payload.cost_per_hour,
            extra_cost_per_hour=payload.extra_cost_per_hour,
            cost_for_addon_km=payload.cost_for_addon_km,
            extra_cost_for_addon_km=payload.extra_cost_for_addon_km,
            pickup_notes=payload.pickup_notes or "",
        )

        # estimate/vendor are derived in calculate_hourly_fare; for the master order, we can echo the inputs
        master_order = create_master_from_hourly(
            db,
            order,
            pick_near_city=payload.pick_near_city,
            trip_time=str(payload.package_hours.get("hours", 0)),
            estimated_price=fare["fare"].estimate_price if isinstance(fare, dict) else fare.fare.estimate_price,
            vendor_price=fare["fare"].vendor_amount if isinstance(fare, dict) else fare.fare.vendor_amount,
            max_time_to_assign_order=payload.max_time_to_assign_order,
            toll_charge_update=payload.toll_charge_update,
        )

        return {"order_id": master_order.id,
                "order_status": master_order.trip_status,
                "picup_near_city": master_order.pick_near_city,
                "vendor_price" : master_order.vendor_price,
                "estimated_price" : master_order.estimated_price,
                "trip_type" : master_order.trip_type,
                "trip_time" : master_order.trip_time
                }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to confirm hourly order: {str(e)}",
        )


