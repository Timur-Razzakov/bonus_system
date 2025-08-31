from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from apps.core.config import settings


auth_engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.ECHO_SQL,
    connect_args={"server_settings": {"application_name": settings.PROJECT_NAME}},
)
async_session = async_sessionmaker(
    bind=auth_engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)
