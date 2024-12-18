from sqlalchemy.orm import Session
from . import models, schemas

# CRUD operations for Product
def get_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Product).offset(skip).limit(limit).all()

def get_product_by_id(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()

def create_product(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(name=product.name, price=product.price, stock=product.stock)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def update_product(db: Session, product_id: int, product: schemas.ProductUpdate):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not db_product:
        return None

    # Apply updates
    if product.name:
        db_product.name = product.name
    if product.price:
        db_product.price = product.price
    if product.stock:
        db_product.stock = product.stock

    db.commit()
    db.refresh(db_product)
    return db_product

def delete_product(db: Session, product_id: int):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if db_product:
        db.delete(db_product)
        db.commit()

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
    db_order = models.Order(customer_id=order.customer_id, total_price=0)
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

def get_orders_with_details(db: Session, skip: int = 0, limit: int = 100):
    orders = db.query(models.Order).offset(skip).limit(limit).all()
    detailed_orders = []

    for order in orders:
        order_details = {
            "id": order.id,
            "customer": {
                "id": order.customer.id,
                "name": order.customer.name,
                "email": order.customer.email,
            },
            "total_price": order.total_price,
            "items": []
        }
        for item in order.items:
            product = db.query(models.Product).filter(models.Product.id == item.product_id).first()
            order_details["items"].append({
                "product_id": product.id,
                "product_name": product.name,
                "quantity": item.quantity,
                "price": item.price
            })
        detailed_orders.append(order_details)

    return detailed_orders
