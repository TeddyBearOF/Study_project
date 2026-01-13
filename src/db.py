from contextlib import  asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker


from src.config import Settings

settings = Settings()
engine = create_async_engine(str(settings.postgres_url))


@asynccontextmanager
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async_session = async_sessionmaker(
        engine,
        expire_on_commit=False,
        class_=AsyncSession
    )

    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()