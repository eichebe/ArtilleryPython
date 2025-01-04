from pydantic import BaseModel
from typing import List, Optional

# Category schema
class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    name: Optional[str]

    class Config:
        from_attributes = True

class Category(CategoryBase):
    id: int

    class Config:
        from_attributes = True

# Product schema
class ProductBase(BaseModel):
    name: str
    description: Optional[str]  # Fixed schema to match the model
    price: float
    stock: int
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

# Customer schema
class CustomerBase(BaseModel):
    name: str
    email: str
    phone: str

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(BaseModel):
    name: Optional[str]
    email: Optional[str]
    phone: Optional[str]

    class Config:
        from_attributes = True

class Customer(CustomerBase):
    id: int

    class Config:
        from_attributes = True

# Order Item schema
class OrderItemBase(BaseModel):
    product_id: int
    quantity: int
    price: float

class OrderItemCreate(OrderItemBase):
    pass

class OrderItemUpdate(BaseModel):
    product_id: Optional[int]
    quantity: Optional[int]
    price: Optional[float]

    class Config:
        from_attributes = True

class OrderItem(OrderItemBase):
    id: int

    class Config:
        from_attributes = True

# Order schema
class OrderBase(BaseModel):
    customer_id: int

class OrderCreate(OrderBase):
    items: List[OrderItemCreate]

class OrderUpdate(BaseModel):
    customer_id: Optional[int]
    total_price: Optional[float]
    items: Optional[List[OrderItemUpdate]]

    class Config:
        from_attributes = True

class OrderWithDetails(OrderBase):
    id: int
    total_price: float
    items: List[OrderItem]

    class Config:
        from_attributes = True

class Order(OrderBase):
    id: int
    total_price: float

    class Config:
        from_attributes = True

class BulkOrderCreate(BaseModel):
    orders: List[OrderCreate]
