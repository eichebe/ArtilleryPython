from pydantic import BaseModel
from typing import List, Optional

# Product schema
class ProductBase(BaseModel):
    name: str
    price: float
    stock: int

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int
    
    class Config:
        orm_mode = True

# Customer schema
class CustomerBase(BaseModel):
    name: str
    email: str
    phone: str

class CustomerCreate(CustomerBase):
    pass

class Customer(CustomerBase):
    id: int
    
    class Config:
        orm_mode = True

# Order schema
class OrderItemBase(BaseModel):
    product_id: int
    quantity: int
    price: float

class OrderCreate(BaseModel):
    customer_id: int
    items: List[OrderItemBase]

class Order(OrderCreate):
    id: int
    total_price: float

    class Config:
        orm_mode = True
