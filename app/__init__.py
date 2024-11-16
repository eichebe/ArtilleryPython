# __init__.py

# Import models
from .models import Product, Customer, Order

# Import schemas
from .schemas import ProductCreate, CustomerCreate, OrderCreate
from .schemas import ProductUpdate, CustomerUpdate, OrderUpdate

# Import services
from .services import create_product, create_customer, create_order
from .services import update_product, update_customer, update_order
from .services import delete_product, delete_customer, delete_order

