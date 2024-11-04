from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine

from config import settings

SQLALCHEMY_DATABASE_URL = (
    f"postgresql+asyncpg:"
    f"//{settings.database_username}"
    f":{settings.database_password}"
    f"@{settings.database_hostname}"
    f":{settings.database_port}"
    f"/{settings.database_name}"
)

engine = create_async_engine(url=SQLALCHEMY_DATABASE_URL, echo=True)
AsyncSessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
