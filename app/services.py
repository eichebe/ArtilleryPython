from sqlalchemy.orm import Session

from .app import models
from .app import schemas

# CRUD operations for Product
def get_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Product).offset(skip).limit(limit).all()

def create_product(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(name=product.name, price=product.price, stock=product.stock)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

# CRUD operations for Customer
def get_customers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Customer).offset(skip).limit(limit).all()

def create_customer(db: Session, customer: schemas.CustomerCreate):
    db_customer = models.Customer(name=customer.name, email=customer.email, phone=customer.phone)
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

# CRUD operations for Order
def create_order(db: Session, order: schemas.OrderCreate):
    db_order = models.Order(customer_id=order.customer_id, total_price=0)  # Initial total price will be calculated
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    
    total_price = 0
    for item in order.items:
        db_item = models.OrderItem(order_id=db_order.id, product_id=item.product_id, quantity=item.quantity, price=item.price)
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        total_price += item.quantity * item.price

    db_order.total_price = total_price
    db.commit()
    db.refresh(db_order)

    return db_order
