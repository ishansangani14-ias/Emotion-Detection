"""
Database connection and session management
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Get settings - import here to avoid circular import
def get_database_url():
    try:
        from backend.config import settings
        return settings.DATABASE_URL
    except:
        return "postgresql://admin:password123@localhost:5432/emotion_db"

# Create database engine
engine = create_engine(
    get_database_url(),
    pool_size=20,
    max_overflow=10,
    pool_pre_ping=True,
    echo=False
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for models
Base = declarative_base()


def get_db():
    """
    Dependency for getting database session
    Usage: db: Session = Depends(get_db)
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database - create all tables"""
    Base.metadata.create_all(bind=engine)
