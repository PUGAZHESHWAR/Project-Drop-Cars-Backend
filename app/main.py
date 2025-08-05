from fastapi import FastAPI
from app.api.routes import vendor
from app.database.session import Base, engine

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Auth API")

app.include_router(vendor.router, prefix="/api/users", tags=["Users"])
