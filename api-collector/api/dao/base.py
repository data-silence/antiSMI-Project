from sqlalchemy import insert, select
from sqlalchemy.exc import SQLAlchemyError

from api.db import asmi_async_session_maker
from loguru import logger


class BaseDao:
    """This Class is Data Access Object for common db requests to any tables"""
    model = None

    @classmethod
    async def get_by_id(cls, model_id: int):
        """Get record by id"""
        async with asmi_async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(id=model_id)
            result = await session.execute(query)
            return result.mappings.one_or_none()

    @classmethod
    async def get_one_or_none(cls, **filter_by):
        """Get only one record or None for select request with filter"""
        async with asmi_async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(**filter_by)
            result = await session.execute(query)
            return result.mappings().one_or_none()

    @classmethod
    async def get_all(cls, **filter_by):
        """Get all records for select request with filter"""
        async with asmi_async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(**filter_by)
            result = await session.execute(query)
            return result.mappings().all()

    @classmethod
    async def add(cls, **data):
        try:
            query = insert(cls.model).values(**data).returning(cls.model.id)
            async with asmi_async_session_maker() as session:
                result = await session.execute(query)
                await session.commit()
                return result.mappings().first()
        except (SQLAlchemyError, Exception) as e:
            msg = ''
            if isinstance(e, SQLAlchemyError):
                msg = "Database Exc: Cannot insert data into table"
            elif isinstance(e, Exception):
                msg = "Unknown Exc: Cannot insert data into table"
            logger.error(msg, extra={"table": cls.model.__tablename__})
            return None
