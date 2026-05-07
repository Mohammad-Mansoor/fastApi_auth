from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from core.exceptions.app_exception import AppException
from core.schemas import QueryOptionsDto
from .repository import UserRepository
from .models import UserNotifications
from .schemas import UserCreate,UserOut
from common.utils.generatePassword import generate_password
from core.security import hash_password
from infrastructure.redis.service import RedisCacheService
from infrastructure.redis.keys import SessionCacheKeys, UsersCacheKeys
from common.query_builder.query_builder import QueryConfig

class UserService:

    def __init__(self):
        self.userRepo = UserRepository()
        self.redisCacheService = RedisCacheService()
        

    async def createUser(self, db: AsyncSession, data: UserCreate):
        user_list_prefex = UsersCacheKeys.users_list(None, is_prefix=True)

        try:
            existing = await self.userRepo.get_user_by_email(db, data.email)
            if existing:
                raise AppException(

                    status_code=409,
                    message="Email already exists",
                    error="EMAIL_ALREADY_EXISTS"
                )

            generatedPassword = generate_password(8)
            print("✅ PASSWORD:", generatedPassword)

            hashed_password = hash_password(generatedPassword)

            user_data = data.model_dump()
            user_data["password"] = hashed_password

            # 🧱 create user
            new_user = await self.userRepo.createUser(db, user_data)

            # 🔔 notifications (relationship)
            new_user.notifications = UserNotifications(
                isWhatsappOn=False,
                isTelegramOn=False,
                isEmailOn=True,
                isInAppOn=True
            )

            # 💾 transaction
            await db.commit()
            await db.refresh(new_user)
            await self.redisCacheService.del_by_prefix(user_list_prefex)
            response = {
                "success": True,
                "message": "User Created Successfully.",
                "data": new_user
            }
            return response

        except Exception as e:
            await db.rollback()
            raise e
        
        
    async def get_user_by_id(self, db: AsyncSession, userId: str):
        sing_user_cache_key = UsersCacheKeys.users_single(userId)
        print("this is userid inside serviec: ", userId)
        async def queryDB ():
            user = await self.userRepo.get_user_by_id(db, userId)
            clean_value = UserOut.model_validate(user).model_dump()
            return clean_value
        
        result = await self.redisCacheService.get_or_set(sing_user_cache_key, queryDB)
        print(f"single user✅✅✅: {result}")    
        return result
    
    async def get_all_users(self, db:AsyncSession, request: Request, options: QueryOptionsDto = Depends()):
        merged_queries = {
            **dict(request.query_params),
            **options.model_dump(exclude_none=True)
        }
        search_able_feilds = [
            "firstName",
            "lastName",
            "email",
            "whatsapp",
            "telegramUsername"
        ]
        filterable_fields = {
            
            "isActive": "isActive",

            "isWhatsappOn": "notifications.isWhatsappOn",

            "isTelegramOn": "notifications.isTelegramOn",

            "isEmailOn": "notifications.isEmailOn",

            "isInAppOn": "notifications.isInAppOn",
            
        }
        
        select_fields=[
            "id",
            "firstName",
            "lastName",
            "email"
        ]
        
        queryConfig= QueryConfig(
            searchable_fields= search_able_feilds,
            filterable_fields = filterable_fields,
            # select_fields=select_fields,
            default_sort="createdAt:DESC",
        )
        
        result = await self.userRepo.get_all_users(db,merged_queries, queryConfig )
        return result