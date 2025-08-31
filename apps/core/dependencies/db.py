from collections.abc import AsyncGenerator
from typing import Annotated, Any

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from apps.core.database import async_session


async def get_db_session() -> AsyncGenerator[AsyncSession, Any]:
    async with async_session() as session:
        yield session
        await session.close()


DBSessionDep = Annotated[AsyncSession, Depends(get_db_session)]
