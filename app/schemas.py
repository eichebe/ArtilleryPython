from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional

# Category schemas
class CategoryBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)

class Category(CategoryBase):
    id: int

    class Config:
        from_attributes = True

# Product schemas
class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str]
    price: float = Field(..., ge=0)
    stock: int = Field(..., ge=0)
    category_id: int

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    price: Optional[float]
    stock: Optional[int]
    category_id: Optional[int]

    class Config:
        from_attributes = True

class Product(ProductBase):
    id: int

    class Config:
        from_attributes = True

# Customer schemas
class CustomerBase(BaseModel):
    name: str
    email: EmailStr
    phone: str = Field(..., min_length=7, max_length=20)

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(BaseModel):
    name: Optional[str]
    email: Optional[EmailStr]
    phone: Optional[str]

    class Config:
        from_attributes = True

class Customer(CustomerBase):
    id: int

    class Config:
        from_attributes = True

#OrderItems Schema
class OrderItem(BaseModel):
    product_id: int
    quantity: int
    price: float

    class Config:
        from_attributes = True


class OrderItemCreate(BaseModel):
    pass

class OrderItemUpdate(BaseModel):
    product_id: Optional[int]
    quantity: Optional[int]
    price: Optional[float]

    class Config:
        from_attributes = True


class OrderUpdate(BaseModel):
    customer_id: Optional[int]
    items: Optional[List[OrderItemUpdate]]

    class Config:
        from_attributes = True

#Order Schema
class Order(BaseModel):
    id: int
    customer_id: int
    total_price: float
    items: List[OrderItem]

    class Config:
        from_attributes = True


class OrderCreate(BaseModel):
    items: List[OrderItemCreate]

class OrderUpdate(BaseModel):
    customer_id: Optional[int]
    total_price: Optional[float]
    items: Optional[List[OrderItemUpdate]]

    class Config:
        from_attributes = True

class Order(BaseModel):
    id: int
    customer_id: int
    total_price: float
    items: List[OrderItem]

    class Config:
        from_attributes = True