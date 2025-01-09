from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import List
import logging
from fastapi.middleware.cors import CORSMiddleware

from app import models, schemas
from app import services

# Database setup
DATABASE_URL = "mysql+pymysql://root:@localhost:3306/loadtest_db"
engine = create_engine(DATABASE_URL, pool_recycle=3600)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
models.Base.metadata.create_all(bind=engine)

# Initialize app
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # List of allowed origins, use ["*"] to allow all origins
    allow_credentials=True,  # Allow cookies and authentication headers
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers
)
# Logging setup
logger = logging.getLogger("fastapi")
logging.basicConfig(level=logging.INFO)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Category Routes
@app.post("/categories", response_model=schemas.Category)
def create_category(category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    return services.create_category(db=db, category=category)

@app.get("/categories", response_model=List[schemas.Category])
def read_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return services.get_categories(db=db, skip=skip, limit=limit)

@app.put("/categories/{category_id}", response_model=schemas.Category)
def update_category_route(
    category_id: int, 
    category: schemas.CategoryUpdate, 
    db: Session = Depends(get_db)
):
    return services.update_category(db=db, category_id=category_id, category=category)

@app.delete("/categories/{category_id}")
def delete_category(category_id: int, db: Session = Depends(get_db)):
    return services.delete_category(db=db, category_id=category_id)

# Product Routes
@app.post("/products", response_model=schemas.Product)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    return services.create_product(db=db, product=product)

@app.get("/products/{product_id}", response_model=schemas.Product)
def read_product(product_id: int, db: Session = Depends(get_db)):
    return services.get_product_by_id(db, product_id)

@app.put("/products/{product_id}", response_model=schemas.Product)
def update_product_route(
    product_id: int, 
    product: schemas.ProductUpdate, 
    db: Session = Depends(get_db)
):
    updated_product = services.update_product(db=db, product_id=product_id, product=product)
    if updated_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated_product

@app.get("/products", response_model=List[schemas.Product])
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return services.get_products(db=db, skip=skip, limit=limit)

@app.get("/products/{product_id}", response_model=schemas.Product)
def read_product(product_id: int, db: Session = Depends(get_db)):
    return services.get_product_by_id(db, product_id)

@app.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    return services.delete_product(db=db, product_id=product_id)

# Customer Routes
@app.post("/customers", response_model=schemas.Customer)
def create_customer(customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    return services.create_customer(db=db, customer=customer)

@app.get("/customers", response_model=List[schemas.Customer])
def read_customers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return services.get_customers(db=db, skip=skip, limit=limit)

@app.get("/customers/{customer_id}", response_model=schemas.Customer)
def read_customer(customer_id: int, db: Session = Depends(get_db)):
    return services.get_customer_by_id(db, customer_id)

@app.put("/customers/{customer_id}", response_model=schemas.Customer)
def update_customer_route(
    customer_id: int, 
    customer: schemas.CustomerUpdate, 
    db: Session = Depends(get_db)
):
    updated_customer = services.update_customer(db=db, customer_id=customer_id, customer=customer)
    if not updated_customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return updated_customer


@app.delete("/customers/{customer_id}")
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    return services.delete_customer(db=db, customer_id=customer_id)

# Order Routes
@app.post("/orders", response_model=schemas.Order)
def create_order(order_data: dict, db: Session = Depends(get_db)):
    return services.create_order(db=db, order_data=order_data)

@app.get("/orders/{order_id}", response_model=schemas.Order)
def read_order(order_id: int, db: Session = Depends(get_db)):
    return services.get_order_by_id(db, order_id)

@app.delete("/orders/{order_id}")
def delete_order(order_id: int, db: Session = Depends(get_db)):
    return services.delete_order(db=db, order_id=order_id)

@app.put("/orders/{order_id}", response_model=schemas.Order)
def update_order_route(order_id: int, order: schemas.OrderUpdate, db: Session = Depends(get_db)):
    return services.update_order(db=db, order_id=order_id, order=order)

@app.get("/orders/report/{customer_id}")
def generate_order_report(customer_id: int, db: Session = Depends(get_db)):
    return services.generate_customer_order_report(db=db, customer_id=customer_id)

@app.get("/orders/customer/{customer_id}/report", response_model=List[schemas.Order])
def get_customer_order_report(customer_id: int, db: Session = Depends(get_db)):
    return services.get_customer_order_report(db=db, customer_id=customer_id)
