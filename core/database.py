from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from core.config import settings

# =========================
# 1. CREATE ENGINE
# =========================
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,   # logs SQL queries in dev
    pool_pre_ping=True,    # checks DB connection health
)

# =========================
# 2. SESSION FACTORY
# =========================
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# =========================
# 3. BASE MODEL
# =========================
Base = declarative_base()


async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()



# HOW YOU USE IT IN CONTROLLERS
# from fastapi import Depends
# from sqlalchemy.ext.asyncio import AsyncSession
# from app.core.dependencies import get_db

# @app.post("/login")
# async def login(db: AsyncSession = Depends(get_db)):


# HOW MODELS CONNECT
# from sqlalchemy import Column, Integer, String
# from app.core.database import Base

# class User(Base):
#     __tablename__ = "users"

#     id = Column(Integer, primary_key=True)
#     email = Column(String, unique=True)
#     password = Column(String)