from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./blog.db"

# Create async engine. Engine = manages database connections
engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread":False}, # Allows SQLite to be used across threads/tasks
)

# Create async session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession, # tells SQLAlchemy to use AsyncSession class
    expire_on_commit=False, # prevents objects from becoming "expired" after commit (so they can still be used)
)


# Declarative Base class. All ORM models (tables) will inherit from this Base
class Base(DeclarativeBase):
    pass


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session