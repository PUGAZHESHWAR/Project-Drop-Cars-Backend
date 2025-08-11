from sqlalchemy import Column, String, Enum as SqlEnum, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
import uuid
import enum
from app.database.session import Base

class AccountStatusEnum(enum.Enum):
    ACTIVE = "Active"
    INACTIVE = "Inactive"
    PENDING = "Pending"

class User(Base):
    __tablename__ = "vendors"

    # id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, index=True)
    full_name = Column(String, nullable=False)
    organization_id = Column(String, nullable=False)
    mobile_number = Column(String(10), unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    account_status = Column(
        SqlEnum(AccountStatusEnum, name="account_status_enum"),
        default=AccountStatusEnum.INACTIVE,
        nullable=False
    )
    created_at = Column(TIMESTAMP)