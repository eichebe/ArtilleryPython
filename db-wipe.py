from sqlalchemy import create_engine
from app.models import Base
from email_validator import validate_email  # type: ignore 

DATABASE_URL = "mysql+pymysql://root:@localhost:3306/loadtest_db"

def reset_database():
    engine = create_engine(DATABASE_URL)

    # Drop all tables
    print("Dropping all tables...")
    Base.metadata.drop_all(bind=engine)

    # Recreate all tables
    print("Recreating all tables...")
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    reset_database()
