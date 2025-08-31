import datetime

from sqlalchemy import BigInteger, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column


class Base(DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"


class BaseModel(Base):
    __abstract__ = True
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(), server_default=func.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime(), server_default=func.now())
