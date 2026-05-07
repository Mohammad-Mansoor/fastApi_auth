from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db
from core.schemas import QueryOptionsDto
from .service import UserService
from .schemas import UserCreate, CreateUserResponse

router = APIRouter()
service = UserService()


@router.post("/users", response_model = CreateUserResponse)
async def create_user(data: UserCreate, db: AsyncSession = Depends(get_db)):
    return await service.createUser(db, data)


@router.get("/users/{userid}")
async def get_single_user(userid: str, db:AsyncSession = Depends(get_db)):
    print("userid in the controller: ", userid)
    return await service.get_user_by_id(db, userid)

@router.get("/users")
async def get_all_users( request: Request,db:AsyncSession = Depends(get_db), options:QueryOptionsDto = Depends() ):
    return await service.get_all_users(db, request, options)
    ...