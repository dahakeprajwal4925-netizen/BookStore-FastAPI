from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database import Base


class Order(Base):

    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)

    customer_name = Column(String(100), nullable=False)

    email = Column(String(100), nullable=False)

    phone = Column(String(15), nullable=False)

    address = Column(String(500), nullable=False)

    total_amount = Column(Float, nullable=False)

    status = Column(String(50), default="Pending")

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationship with OrderItem
    items = relationship(
        "OrderItem",
        back_populates="order",
        cascade="all, delete-orphan"
    )