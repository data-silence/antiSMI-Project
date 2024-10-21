"""
This is database connection module
"""

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from api.config import settings

asmi_engine = create_async_engine(settings.ASMI_URL)
asmi_async_session_maker = async_sessionmaker(asmi_engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass
