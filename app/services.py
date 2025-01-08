from typing import List
from sqlalchemy.orm import Session
from fastapi import HTTPException
from . import models, schemas

# Category CRUD
def create_category(db: Session, category: schemas.CategoryCreate):
    db_category = models.Category(name=category.name)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def update_category(db: Session, category_id: int, category: schemas.CategoryUpdate):
    db_category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    if category.name:
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

def get_product_by_id(db: Session, product_id: int):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

def update_product(db: Session, product_id: int, product: schemas.ProductUpdate):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")

    if product.name:
        db_product.name = product.name
    if product.description:
        db_product.description = product.description
    if product.price:
        db_product.price = product.price
    if product.stock:
        db_product.stock = product.stock
    if product.category_id:
        db_product.category_id = product.category_id

    db.commit()
    db.refresh(db_product)
    return db_product

def get_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Product).offset(skip).limit(limit).all()

def get_product_by_id(db: Session, product_id: int):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

def delete_product(db: Session, product_id: int):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(db_product)
    db.commit()
    return {"message": f"Product with ID {product_id} deleted"}

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

def get_customers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Customer).offset(skip).limit(limit).all()

def get_customer_by_id(db: Session, customer_id: int):
    db_customer = db.query(models.Customer).filter(models.Customer.id == customer_id).first()
    if not db_customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return db_customer


def delete_customer(db: Session, customer_id: int):
    db_customer = db.query(models.Customer).filter(models.Customer.id == customer_id).first()
    if not db_customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    db.delete(db_customer)
    db.commit()
    return {"message": f"Customer with ID {customer_id} deleted"}

def update_customer(db: Session, customer_id: int, customer: schemas.CustomerUpdate):
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

# Order CRUD
def create_order(db: Session, order: schemas.OrderCreate):
    # Create the base order with the customer ID
    db_order = models.Order(customer_id=order.customer_id, total_price=0)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    total_price = 0

    # Process all items in the order
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

        # Deduct stock from the product
        product.stock -= item.quantity

        # Create order item
        db_item = models.OrderItem(
            order_id=db_order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            price=item.price
        )
        db.add(db_item)

        # Update the total price for the order
        total_price += item.quantity * item.price

    # Update total price in the order
    db_order.total_price = total_price
    db.commit()
    db.refresh(db_order)

    return {
        "order_id": db_order.id,
        "customer_id": db_order.customer_id,
        "total_price": db_order.total_price,
        "items": [{"product_id": i.product_id, "quantity": i.quantity, "price": i.price} for i in db_order.items]
    }

def get_order_by_id(db: Session, order_id: int):
    db_order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    return {
        "id": db_order.id,
        "customer_id": db_order.customer_id,
        "total_price": db_order.total_price,
        "items": [
            {"product_id": item.product_id, "quantity": item.quantity, "price": item.price}
            for item in db_order.items
        ],
    }

def get_orders_with_details(db: Session, skip: int = 0, limit: int = 100):
    orders = db.query(models.Order).offset(skip).limit(limit).all()
    detailed_orders = [
        {
            "id": order.id,
            "customer_id": order.customer_id,
            "total_price": order.total_price,
            "items": [
                {
                    "product_id": item.product_id,
                    "quantity": item.quantity,
                    "price": item.price,
                }
                for item in order.items
            ]
        }
        for order in orders
    ]
    return detailed_orders

def delete_order(db: Session, order_id: int):
    db_order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    db.delete(db_order)
    db.commit()
    return {"message": f"Order with ID {order_id} deleted"}

def create_bulk_orders(db: Session, bulk_orders: List[schemas.OrderCreate]):
    responses = []
    for order in bulk_orders:
        responses.append(create_order(db, order))
    return responses

def update_order(db: Session, order_id: int, order: schemas.OrderUpdate):
    db_order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")

    # Update customer_id if provided
    if order.customer_id is not None:
        db_order.customer_id = order.customer_id

    # Update order items if provided
    if order.items:
        # Clear current items
        db.query(models.OrderItem).filter(models.OrderItem.order_id == order_id).delete()

        total_price = 0
        for item in order.items:
            # Validate the product exists
            product = db.query(models.Product).filter(models.Product.id == item.product_id).first()
            if not product:
                raise HTTPException(status_code=404, detail=f"Product with ID {item.product_id} not found")
            
            # Check stock availability
            if product.stock < item.quantity:
                raise HTTPException(
                    status_code=400, 
                    detail=f"Insufficient stock for Product ID {item.product_id}. Available: {product.stock}"
                )

            # Deduct stock and create new order item
            product.stock -= item.quantity
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
