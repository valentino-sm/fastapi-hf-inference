from contextlib import asynccontextmanager
from contextvars import ContextVar
from typing import Protocol

from sqlalchemy.ext.asyncio.session import AsyncSession

from infrastructure.db.unitofwork import ABCUnitOfWork


class ABCSessionManager(Protocol):
    @asynccontextmanager
    async def __call__(self) -> None:
        raise NotImplementedError

    def session(self) -> AsyncSession:
        raise NotImplementedError


class SessionManager(ABCSessionManager):
    def __init__(self, uow: ABCUnitOfWork):
        self._uow = uow
        self._ctx_session: ContextVar[AsyncSession] = ContextVar("db_session")

    @asynccontextmanager
    async def __call__(self):
        async with self._uow as session:
            token = self._ctx_session.set(session)
            try:
                yield
            finally:
                self._ctx_session.reset(token)

    def session(self) -> AsyncSession:
        return self._ctx_session.get()
