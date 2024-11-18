from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from databases import Database
from .config import SQLALCHEMY_URL

# Create an async engine for database connection
async_engine = create_async_engine(SQLALCHEMY_URL, echo=True, future=True)

# Database instance for non-SQLAlchemy operations
database = Database(SQLALCHEMY_URL)

# Configure session maker to use async sessions
async_session = sessionmaker(
    bind=async_engine,
    expire_on_commit=False,
    class_=AsyncSession,
    future=True
)

# Base class for declarative models
Base = declarative_base()


async def get_async_db():
    """
    Dependency that provides an async database session.
    """
    async with async_session() as session:
        yield session


async def create_tables():
    """
    Create all tables based on the models defined with SQLAlchemy's Base.
    """
    async with async_engine.begin() as conn:
        # Use run_sync to execute the synchronous metadata create_all method
        await conn.run_sync(Base.metadata.create_all)
