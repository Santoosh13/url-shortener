from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from keyvault import get_secret

#fetch all DB credentials from key vault
DB_HOST = get_secret("DB-HOST")
DB_NAME = get_secret("DB-NAME")
DB_USER = get_secret("DB-username")
DB_PASSWORD = get_secret("DB-PASSWORD")
DB_PORT = get_secret("DB-PORT")


#Build the PostgreSQL connection string
#sslmode = require is mandatory for azure postgreSQL
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?sslmode=require"



engine = create_engine(DATABASE_URL)

#Each request gets its own database session
SessionLocal = sessionmaker(autocommit=False, autoflush = False, bind = engine)

#Base class for all SQLAlchemy models


def get_db():
    """Dependency function for FastAPI endpoints.
        Yeilds a database session and closes it when done.
    """

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()