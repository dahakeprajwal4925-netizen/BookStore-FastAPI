from pydantic import BaseModel, EmailStr, Field, model_validator
from typing import List
from datetime import datetime


class OrderItemCreate(BaseModel):
    book_id: int
    quantity: int = Field(gt=0)


class OrderCreate(BaseModel):
    customer_name: str
    email: EmailStr
    phone: str
    address: str
    items: List[OrderItemCreate] = Field(min_length=1)

    @model_validator(mode="after")
    def check_duplicate_books(self):
        book_ids = [item.book_id for item in self.items]

        if len(book_ids) != len(set(book_ids)):
            raise ValueError("Duplicate book IDs are not allowed in one order")

        return self


class OrderItemResponse(BaseModel):
    id: int
    book_id: int
    quantity: int
    price: float


class OrderResponse(BaseModel):
    id: int
    customer_name: str
    email: EmailStr
    phone: str
    address: str
    total_amount: float
    status: str
    created_at: datetime
    items: List[OrderItemResponse]

    class Config:
        from_attributes = True