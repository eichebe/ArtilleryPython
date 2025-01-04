from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from . import schemas
from . import models

# Category CRUD
def create_category(db: Session, category: schemas.CategoryCreate):
    db_category = models.Category(name=category.name)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def update_category(db: Session, category_id: int, category: schemas.CategoryCreate):
    db_category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    db_category.name = category.name
    db.commit()
    db.refresh(db_category)
    return db_category

def get_categories(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Category).offset(skip).limit(limit).all()

def delete_category(db: Session, category_id: int):
    db_category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    db.delete(db_category)
    db.commit()
    return {"message": f"Category with ID {category_id} deleted"}

# Product CRUD
def create_product(db: Session, product: schemas.ProductCreate):
    try:
        # Validate category_id
        category = db.query(models.Category).filter(models.Category.id == product.category_id).first()
        if not category:
            raise HTTPException(status_code=400, detail="Invalid category ID")

        db_product = models.Product(
            name=product.name, 
            description=product.description, 
            price=product.price, 
            stock=product.stock, 
            category_id=product.category_id
        )
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        return db_product
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error creating product") from e

from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from sqlalchemy.orm import Session
from . import models, schemas

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

def get_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Product).offset(skip).limit(limit).all()

def get_product_by_id(db: Session, product_id: int):
    try:
        db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
        if not db_product:
            raise HTTPException(status_code=404, detail="Product not found")
        return db_product
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Error retrieving product") from e


def delete_product(db: Session, product_id: int):
    try:
        db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
        if not db_product:
            raise HTTPException(status_code=404, detail="Product not found")
        db.delete(db_product)
        db.commit()
        return {"message": f"Product with ID {product_id} deleted"}
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error deleting product") from e

# Customer CRUD
def create_customer(db: Session, customer: schemas.CustomerCreate):
    db_customer = models.Customer(
        name=customer.name, 
        email=customer.email, 
        phone=customer.phone
    )
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

def update_customer(db: Session, customer_id: int, customer: schemas.CustomerCreate):
    db_customer = db.query(models.Customer).filter(models.Customer.id == customer_id).first()
    if not db_customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    if customer.name is not None:
        db_customer.name = customer.name
    if customer.email is not None:
        db_customer.email = customer.email
    if customer.phone is not None:
        db_customer.phone = customer.phone
    db.commit()
    db.refresh(db_customer)
    return db_customer

def get_customers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Customer).offset(skip).limit(limit).all()

def delete_customer(db: Session, customer_id: int):
    db_customer = db.query(models.Customer).filter(models.Customer.id == customer_id).first()
    if not db_customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    db.delete(db_customer)
    db.commit()
    return {"message": f"Customer with ID {customer_id} deleted"}

# Order CRUD
def create_order(db: Session, order: schemas.OrderCreate):
    db_order = models.Order(customer_id=order.customer_id, total_price=0)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    total_price = 0
    for item in order.items:
        db_item = models.OrderItem(
            order_id=db_order.id, 
            product_id=item.product_id, 
            quantity=item.quantity, 
            price=item.price
        )
        db.add(db_item)
        total_price += item.quantity * item.price

    db_order.total_price = total_price
    db.commit()
    db.refresh(db_order)
    return db_order

def update_order(db: Session, order_id: int, order: schemas.OrderCreate):
    db_order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    db_order.total_price = sum(
        item.quantity * item.price for item in order.items
    )
    db.commit()
    db.refresh(db_order)
    return db_order

def get_orders_with_details(db: Session, skip: int = 0, limit: int = 100):
    orders = db.query(models.Order).offset(skip).limit(limit).all()
    detailed_orders = []
    for order in orders:
        items = [
            {
                "product_id": item.product_id,
                "quantity": item.quantity,
                "price": item.price,
            }
            for item in order.items
        ]
        detailed_orders.append({
            "id": order.id,
            "customer_id": order.customer_id,
            "total_price": order.total_price,
            "items": items
        })
    return detailed_orders

def delete_order(db: Session, order_id: int):
    db_order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    db.delete(db_order)
    db.commit()
    return {"message": f"Order with ID {order_id} deleted"}

def generate_customer_order_report(db: Session, customer_id: int):
    customer = db.query(models.Customer).filter(models.Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    orders = db.query(models.Order).filter(models.Order.customer_id == customer_id).all()
    return {
        "customer": customer.name,
        "orders": [{"id": o.id, "total_price": o.total_price} for o in orders]
    }

def create_bulk_orders(db: Session, bulk_orders: List[schemas.OrderCreate]):
    bulk_response = []
    try:
        for order in bulk_orders:
            # Validate customer existence
            customer = db.query(models.Customer).filter(models.Customer.id == order.customer_id).first()
            if not customer:
                raise HTTPException(status_code=404, detail=f"Customer with ID {order.customer_id} not found")
            
            # Create order
            db_order = models.Order(customer_id=order.customer_id, total_price=0)
            db.add(db_order)
            db.commit()
            db.refresh(db_order)

            # Process order items
            total_price = 0
            for item in order.items:
                # Validate product existence
                product = db.query(models.Product).filter(models.Product.id == item.product_id).first()
                if not product:
                    raise HTTPException(status_code=404, detail=f"Product with ID {item.product_id} not found")

                # Check stock availability
                if product.stock < item.quantity:
                    raise HTTPException(
                        status_code=400, 
                        detail=f"Insufficient stock for Product ID {item.product_id}. Available: {product.stock}"
                    )

                # Deduct stock and add order item
                product.stock -= item.quantity
                db_item = models.OrderItem(
                    order_id=db_order.id,
                    product_id=item.product_id,
                    quantity=item.quantity,
                    price=item.price
                )
                db.add(db_item)
                total_price += item.quantity * item.price

            # Update total price for the order
            db_order.total_price = total_price
            db.commit()
            db.refresh(db_order)

            bulk_response.append({
                "order_id": db_order.id,
                "customer_id": db_order.customer_id,
                "total_price": db_order.total_price
            })

        return bulk_response

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to process bulk orders") from e