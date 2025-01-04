from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import List
import logging
from fastapi.middleware.cors import CORSMiddleware

from . import models, schemas
from . import services

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

@app.delete("/categories/{category_id}")
def delete_category(category_id: int, db: Session = Depends(get_db)):
    return services.delete_category(db=db, category_id=category_id)

# Product Routes
@app.post("/products", response_model=schemas.Product)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    return services.create_product(db=db, product=product)

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

@app.delete("/customers/{customer_id}")
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    return services.delete_customer(db=db, customer_id=customer_id)

# Order Routes
@app.post("/orders", response_model=schemas.Order)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    return services.create_order(db=db, order=order)

@app.get("/orders/detailed")
def read_orders_with_details(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return services.get_orders_with_details(db=db, skip=skip, limit=limit)

@app.delete("/orders/{order_id}")
def delete_order(order_id: int, db: Session = Depends(get_db)):
    return services.delete_order(db=db, order_id=order_id)

@app.get("/orders/report/{customer_id}")
def generate_order_report(customer_id: int, db: Session = Depends(get_db)):
    return services.generate_customer_order_report(db=db, customer_id=customer_id)

@app.post("/orders/bulk", response_model=List[dict])
def create_bulk_order(
    bulk_order: schemas.BulkOrderCreate, 
    db: Session = Depends(get_db)
):
    return services.create_bulk_orders(db=db, bulk_orders=bulk_order.orders)

@app.post("/test")
def test_post():
    return {"message": "POST request works!"}