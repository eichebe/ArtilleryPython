from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import List

from . import models, schemas
from . import services

# Database setup
DATABASE_URL = "mysql+pymysql://root:@localhost:3306/loadtest_db"
engine = create_engine(DATABASE_URL, pool_recycle=3600)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Routes for Products
@app.post("/products", response_model=schemas.Product)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    return services.create_product(db=db, product=product)

@app.get("/products", response_model=List[schemas.Product])
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return services.get_products(db=db, skip=skip, limit=limit)

@app.patch("/products/{product_id}", response_model=schemas.Product)
def update_product(product_id: int, product: schemas.ProductUpdate, db: Session = Depends(get_db)):
    db_product = services.get_product_by_id(db=db, product_id=product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return services.update_product(db=db, product_id=product_id, product=product)

@app.delete("/products/{product_id}", response_model=dict)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    db_product = services.get_product_by_id(db=db, product_id=product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    services.delete_product(db=db, product_id=product_id)
    return {"message": f"Product with ID {product_id} has been deleted."}

# Routes for Customers
@app.post("/customers", response_model=schemas.Customer)
def create_customer(customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    return services.create_customer(db=db, customer=customer)

@app.get("/customers", response_model=List[schemas.Customer])
def read_customers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return services.get_customers(db=db, skip=skip, limit=limit)

# Routes for Orders
@app.post("/orders", response_model=schemas.Order)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    return services.create_order(db=db, order=order)

@app.get("/orders/detailed", response_model=List[schemas.OrderWithDetails])
def read_orders_with_details(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return services.get_orders_with_details(db=db, skip=skip, limit=limit)
