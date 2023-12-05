from contextlib import AbstractAsyncContextManager
from typing import Any

from sqlalchemy.ext.asyncio import async_sessionmaker

from infrastructure.db.engine import ABCDatabaseEngine


class ABCUnitOfWork(AbstractAsyncContextManager[Any]):
    ...


class SQLAlchemyUnitOfWork(ABCUnitOfWork):
    def __init__(self, db_engine: ABCDatabaseEngine):
        self.db_engine = db_engine
        self.session_factory = async_sessionmaker(bind=db_engine.get_engine())  # type: ignore

    async def __aenter__(self):
        self.session = self.session_factory()
        return self.session

    async def __aexit__(self, 
                        exc_type, exc_val, exc_tb):
        self.session.expunge_all()
        if exc_type is not None:
            await self.session.rollback()
        else:
            await self.session.commit()
        await self.session.close()
