from sqlalchemy import create_engine
from models import Base

DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)


def reset_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    reset_database()
    print("Database reset successfully!")
