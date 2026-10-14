from datetime import datetime

from sqlalchemy import DateTime, Identity, Integer, JSON, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base

class IdempotencyRecord(Base):
    __tablename__ = "idempotency_records"

    id: Mapped[int] = mapped_column(
        Identity(always=True), 
        primary_key=True
    )

    key: Mapped[str] = mapped_column(
        String(255), 
        unique=True, 
        nullable=False
    )
    
    request_hash: Mapped[str] = mapped_column(
        String(64), 
        nullable=False
    )
    
    response_status: Mapped[int] = mapped_column(
        Integer, 
        nullable=False
    )

    response_body: Mapped[dict] = mapped_column(
        JSON, 
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.current_timestamp(),
        nullable=False,
    )