from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import urllib.parse
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database configuration with security validation
def validate_database_url(url: str) -> str:
    """Validate and secure database URL"""
    if not url:
        raise ValueError("Database URL cannot be empty")
    
    # Parse URL to check for security issues
    parsed = urllib.parse.urlparse(url)
    
    # Check for allowed schemes
    allowed_schemes = ['postgresql', 'postgresql+asyncpg', 'sqlite', 'mysql']
    if parsed.scheme not in allowed_schemes:
        raise ValueError(f"Unsupported database scheme: {parsed.scheme}")
    
    # For SQLite, ensure path is safe
    if parsed.scheme == 'sqlite':
        if '..' in parsed.path or parsed.path.startswith('/'):
            # Restrict to relative paths in project directory
            path = parsed.path.lstrip('/')
            if not path.startswith('database/'):
                path = f"database/{path}"
            return f"sqlite:///{path}"
    
    return url

# Get and validate database URL
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./database/vuc2026.db")
DATABASE_URL = validate_database_url(DATABASE_URL)

# Configure engine based on database type
if DATABASE_URL.startswith("postgresql"):
    engine = create_engine(
        DATABASE_URL,
        pool_size=20,
        max_overflow=30,
        pool_pre_ping=True,
        pool_recycle=3600,
        echo=os.getenv("DATABASE_DEBUG", "false").lower() == "true"
    )
else:
    # SQLite configuration with security
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},  # SQLite için gerekli
        pool_size=10,
        max_overflow=20,
        pool_pre_ping=True,
        echo=os.getenv("DATABASE_DEBUG", "false").lower() == "true"
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Initialize database tables"""
    os.makedirs("database", exist_ok=True)
    Base.metadata.create_all(bind=engine)
