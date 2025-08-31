import asyncio

import pytest
from sqlalchemy import event
from sqlalchemy.engine import make_url, URL
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from testcontainers.postgres import PostgresContainer

from apps.core.models.base import Base
from tests.mock_data.factories import BaseFactory


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def pg_container():
    """Поднимаем PostgreSQL однажды на всю сессию."""
    container = PostgresContainer("postgres:16-alpine")
    container.start()
    try:
        yield container
    finally:
        container.stop()


@pytest.fixture(scope="session")
def pg_async_url(pg_container) -> str:
    """Конвертируем sync-URL testcontainers в asyncpg URL."""
    sync_url = make_url(pg_container.get_connection_url())  # postgresql://user:pass@host:port/db
    async_url = URL.create(
        drivername="postgresql+asyncpg",
        username=sync_url.username,
        password=sync_url.password,
        host=sync_url.host,
        port=sync_url.port,
        database=sync_url.database,
    )
    return str(async_url)


@pytest.fixture(scope="session")
async def engine(pg_async_url):
    """AsyncEngine и создание схемы один раз на всю сессию."""
    engine = create_async_engine(pg_async_url, echo=False, future=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    try:
        yield engine
    finally:
        await engine.dispose()


@pytest.fixture()
async def session(engine) -> AsyncSession:
    """
    На каждый тест:
      - один connection + внешняя транзакция
      - внутри — nested transaction (SAVEPOINT)
      - любые session.commit() внутри кода не мешают (savepoint восстанавливается)
    """
    async with engine.connect() as conn:
        outer = await conn.begin()  # внешняя транзакция
        SessionLocal = async_sessionmaker(bind=conn, expire_on_commit=False, autoflush=False)
        async with SessionLocal() as session:
            # старт первого SAVEPOINT
            await session.begin_nested()

            # автопересоздание SAVEPOINT после каждого commit() внутри теста
            def _restart_savepoint(sess, tx):
                if tx.nested and not tx._parent.nested:
                    sess.begin_nested()

            event.listen(session.sync_session, "after_transaction_end", _restart_savepoint)
            try:
                yield session
            finally:
                event.remove(session.sync_session, "after_transaction_end", _restart_savepoint)
                await session.close()
                await outer.rollback()


@pytest.fixture(autouse=True)
async def bind_factories_to_session(session: AsyncSession):
    """
    Автоматически привязываем твоё factory_boy BaseFactory к актуальной сессии
    для каждого теста (важно, т.к. у тебя BaseFactory.set_session есть).
    """
    BaseFactory.set_session(session)
    yield
