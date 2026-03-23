import logging
from typing import Any
from sqlalchemy.orm import sessionmaker, aliased
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy import (
    select,
    func
)
from authors_models import Posts, Authors, Comments, Base as AuthorsBase
from logs_models import Logs, EventTypes, SpaceTypes, Base as LogsBase

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger("DB_MANAGER")

class DatabaseManager:
    def __init__(self, authors_db_url: str, log_db_url: str):
        logger.info("Starting engine...")
        self.authors_engine = create_async_engine(authors_db_url)
        self.logs_engine = create_async_engine(log_db_url)
        self.authors_async_session = sessionmaker(
            self.authors_engine, expire_on_commit=False, class_=AsyncSession
        )
        self.logs_async_session = sessionmaker(
            self.logs_engine, expire_on_commit=False, class_=AsyncSession
        )
        logger.info("Done")

    async def init_db(self):
        logger.info("Initializing connection...")
        try:
            async with self.authors_engine.begin() as conn:
                logger.info("Creating tables in authors db...")
                await conn.run_sync(AuthorsBase.metadata.create_all)

            async with self.logs_engine.begin() as conn:
                logger.info("Creating tables in logs db...")
                await conn.run_sync(LogsBase.metadata.create_all)
        except Exception as e:
            logger.info(f"Error occured during initialization: {str(e)}")

    async def close_db(self):
        logger.info("Closing connection...")
        await self.authors_engine.dispose()
        await self.logs_engine.dispose()

    async def get_general(self, login: str) -> list[dict[str, Any]]:
        async with self.authors_async_session() as session:
            user_id = (await session.execute(
                select(Authors.id).where(Authors.login == login)
            )).scalar()

        if not user_id:
            raise ValueError("Login not found.")

        async with self.logs_async_session() as session:
            date = func.date(Logs.datetime).label("date")
            data = (await session.execute(
                select(
                    date,
                    func.count().filter(EventTypes.name == "login").label("logins"),
                    func.count().filter(EventTypes.name == "logout").label("logouts"),
                    func.count().filter(SpaceTypes.name == "blog").label("actions")
                )
                .join(SpaceTypes, Logs.space_type_id == SpaceTypes.id)
                .join(EventTypes, Logs.event_type_id == EventTypes.id)
                .where(Logs.user_id == user_id)
                .group_by(date)
                .order_by(date)
            )).mappings().all()

        logger.info("Got general data")
        return data

    async def get_comments(self, login: str) -> list[dict[str, Any]]:
        async with self.authors_async_session() as session:
            post_authors = aliased(Authors)
            comment_authors = aliased(Authors)
            data = (await session.execute(
                select(
                    comment_authors.login,
                    Posts.header,
                    post_authors.login.label("author"),
                    func.count(Comments.id).label("comments_num"),
                )
                .join(comment_authors, comment_authors.id == Comments.author_id)
                .where(comment_authors.login == login)
                .join(Posts, Comments.post_id == Posts.id)
                .join(post_authors, post_authors.id == Posts.author_id)
                .group_by(
                    comment_authors.login,
                    Posts.header,
                    post_authors.login,
                )
            )).mappings().all()

            logger.info("Got comments data")
            return data