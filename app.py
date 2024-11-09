from fastapi import FastAPI, HTTPException
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.orm import Session

# Updated MySQL connection URL (you can modify these based on your MySQL setup)
DATABASE_URL = "mysql+pymysql://root:@localhost:3306/loadtest_db"

Base = declarative_base()

# Create the engine to connect to MySQL
engine = create_engine(DATABASE_URL, pool_recycle=3600)

# SessionLocal will create database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Define your Product model
class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

# Create the table(s) in the MySQL database
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI()

# Endpoint to get all products
@app.get("/products")
def read_products():
    with SessionLocal() as session:
        products = session.query(Product).all()
        return products

# Endpoint to create a new product
@app.post("/products")
def create_product(name: str):
    with SessionLocal() as session:
        product = Product(name=name)
        session.add(product)
        session.commit()
        session.refresh(product)
        return product
