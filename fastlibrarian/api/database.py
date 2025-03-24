import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.future import create_engine
from sqlalchemy.orm import sessionmaker

# Database configuration
DATABASE_URL = "postgresql+asyncpg://user:password@localhost/testdb"

# Create engine
engine = create_engine(DATABASE_URL, echo=True, future=True)

# Create a configured "Session" class
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=sqlalchemy.ext.asyncio.AsyncSession,
)

# Create a Base class for our models
Base = declarative_base()


# Create all tables
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# Initialize the database
import asyncio

asyncio.run(init_db())
# Create all tables
Base.metadata.create_all(bind=engine)
