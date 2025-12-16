from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
import os
#from contextlib import contextmanager

# Get database configuration from environment variables
DATABASE_TYPE = os.getenv("DATABASE_TYPE", "sqlite")
DATABASE_URL = os.getenv("DATABASE_URL")

# Connection URL format: dialect+driver://username:password@host:port/database
if DATABASE_URL:
    # Use DATABASE_URL if provided (for PostgreSQL in Docker)
    connection_url = DATABASE_URL
    print(f"Using database from DATABASE_URL: {DATABASE_TYPE}")
elif DATABASE_TYPE == "postgresql":
    # PostgreSQL configuration from individual env vars
    connection_url = URL.create(
        drivername="postgresql+psycopg2",
        username=os.getenv("POSTGRES_USER", "ricagoapi_user"),
        password=os.getenv("POSTGRES_PASSWORD", "changeme123"),
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=int(os.getenv("POSTGRES_PORT", "5432")),
        database=os.getenv("POSTGRES_DB", "ricagoapi")
    )
    print(f"Using PostgreSQL database: {connection_url}")
else:
    # Default to SQLite for local development
    connection_url = URL.create(
        drivername="sqlite",
        database="app/db/ricagoapi.db"
    )
    print("Using SQLite database: app/db/ricagoapi.db")

# Create engine with connection pooling
# SQLite doesn't support connection pooling the same way
if DATABASE_TYPE == "sqlite":
    engine = create_engine(
        connection_url,
        echo=True  # Show SQL in logs (debug)
    )
else:
    engine = create_engine(
        connection_url,
        pool_size=5,
        max_overflow=10,
        pool_pre_ping=True,  # Test connections for liveness
        echo=True  # Show SQL in logs (debug)
    )


# Create session factory (2.0 style)
DBSession = sessionmaker(
    bind = engine,
    autoflush = False,
    expire_on_commit = False,
    future = True  # Enables 2.0 style
)

def get_db():
    db = DBSession()
    try:
        yield db
    finally:
        db.close()

"""
# Usage of Session
@contextmanager
def get_session()-> Generator[Session, None, None]:
    #Yield a session with automatic cleanup
    session = DBSession()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()
"""

class Base(DeclarativeBase):
    pass

# ---- Create Database and Tables if not exists ----
#Base.metadata.create_all(bind = engine)