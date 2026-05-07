from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from .models import User, UserNotifications
from common.query_builder.query_builder import SQLAlchemyQueryHelper,QueryConfig


class UserRepository:

    async def createUser(self, db: AsyncSession, data: dict):
        user = User(**data)

        db.add(user)
        return user

    async def get_user_by_email(self, db: AsyncSession, email: str):
        result = await db.execute(
            select(User).where(User.email == email)
        )
        return result.scalars().first()

    async def get_user_by_id(self, db: AsyncSession, userid):
        result = await db.execute(
            select(User).where(User.id == userid)
        )
        return result.scalars().first()

    async def delete_user(self, db: AsyncSession, user: User):
        await db.delete(user)
        
    async def get_all_users(self, db:AsyncSession, query: dict, queryConfig):
        # query = 
        print("this is queryconfig: ", queryConfig)
        query = SQLAlchemyQueryHelper.for_(
            model= User,
            session= db,
            options=query,
            config =queryConfig
        )
        result = await query.get_many_and_meta()
        return result
