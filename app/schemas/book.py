
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class BookCreate(BaseModel):
    title: str = Field(min_length=2, max_length=100)
    author: str
    category: str
    price: float = Field(gt=0)
    stock: int = Field(ge=0)
    description: Optional[str] = Field(default=None, max_length=500)


class BookUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=2, max_length=100)
    author: Optional[str] = None
    category: Optional[str] = None
    price: Optional[float] = Field(default=None, gt=0)
    stock: Optional[int] = Field(default=None, ge=0)
    description: Optional[str] = Field(default=None, max_length=500)


class BookResponse(BookCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)
