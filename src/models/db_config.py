from asyncio import current_task

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, async_scoped_session, AsyncSession

from src.config import db_settings

DB_URL = f"postgresql+asyncpg://{db_settings.DB_USER}:{db_settings.DB_PASS}@{db_settings.DB_HOST}/{db_settings.DB_NAME}"

class DataBaseHelper:
    def __init__(self, url: str, echo: bool = False):
        self.engine = create_async_engine(
            url=url,
            echo=echo
        )

        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False
        )

    def scoped_sessions(self):
        session = async_scoped_session(
            session_factory=self.session_factory,
            scopefunc=current_task
        )

        return session

    async def get_session_dependency(self) -> AsyncSession:
        session = self.scoped_sessions()
        yield session
        await session.close()


db_helper = DataBaseHelper(url=DB_URL, echo=True)