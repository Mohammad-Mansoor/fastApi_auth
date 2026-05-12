# seeds/super_admin.py

import asyncio
from sqlalchemy import select

from core.database import AsyncSessionLocal
from modules.users.models import User, UserNotifications
from modules.sessions.models import Session
from modules.usersDevices.models import UserDevices
from core.security import hash_password
from core.config import settings


async def create_super_admin():
    async with AsyncSessionLocal() as db:

        try:
            # ✅ CORRECT WAY (Async SQLAlchemy)
            result = await db.execute(
                select(User).where(User.email == settings.EMAIL)
            )

            user = result.scalars().first()

            if user:
                print("✅ Super admin already exists")
                return

            # Create user
            super_admin = User(
                firstName="Super",
                lastName="Admin",
                email=settings.EMAIL,
                password=hash_password(settings.PASSWORD),
                isSuperAdmin=True,
                isActive=True
            )

            db.add(super_admin)
            await db.flush()  # get ID

            notifications = UserNotifications(
                userId=super_admin.id,
                isWhatsappOn=True,
                isTelegramOn=True,
                isEmailOn=True,
                isInAppOn=True
            )

            db.add(notifications)

            await db.commit()

            print("🚀 Super admin created successfully")

        except Exception as e:
            await db.rollback()
            print("❌ Error creating super admin:", e)


if __name__ == "__main__":
    asyncio.run(create_super_admin())