# import asyncio
import time

from sqlalchemy.exc import DBAPIError
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text

from core.config import app_settings, db_echo_mode
from models.base import Base
from models.files_model import Files
from models.users_model import Users

engine = create_async_engine(
    app_settings.database_dsn,
    # "sqlite+aiosqlite:///fastapi.db",
    echo=db_echo_mode,
    future=True,
)
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


async def create_model():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def ping_database():
    async with async_session() as session:
        try:
            start_time = time.time()
            await session.execute(text("SELECT 1"))
            end_time = time.time()
            return end_time - start_time
        except DBAPIError:
            return None


async def find_user_by_name(name: str) -> Users:
    async with async_session() as session:
        query = select(Users).where(Users.name == name)
        user = await session.scalar(query)
        return user


async def create_user(name, hash_password) -> Users:
    async with async_session() as session:
        user = Users(name=name, hash_password=hash_password)
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user


async def add_file(name: str, path: str, size: int, user: Users):
    async with async_session() as session:
        new_file = Files(
            name=name,
            path=path,
            size=size,
            user=user,
            user_id=user.id,
            is_downloadable=True,
        )
        session.add(new_file)
        await session.commit()
        return new_file


async def get_all_user_file(user: Users) -> list:
    async with async_session() as session:
        query = select(Files).where(Files.user == user)
        result = await session.execute(query)
        files = result.scalars().all()
        return files


async def get_file(s_data: str) -> Files:
    async with async_session() as session:
        if s_data.isdigit():
            query = select(Files).where(Files.id == int(s_data))
        else:
            query = select(Files).where(Files.path == s_data)
        file = await session.execute(query)
        return file.scalar()
