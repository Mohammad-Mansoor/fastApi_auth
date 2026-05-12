from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db
from core.schemas import QueryOptionsDto
from .service import UserService
from .schemas import UserCreate, CreateUserResponse,UserListOut,SingleUserOut

router = APIRouter()
service = UserService()


@router.post("/users", response_model = CreateUserResponse)
async def create_user(data: UserCreate, db: AsyncSession = Depends(get_db)):
    return await service.createUser(db, data)


@router.get("/users/{userid}",response_model=SingleUserOut )
async def get_single_user(userid: str, db:AsyncSession = Depends(get_db)):
    print("userid in the controller: ", userid)
    user= await service.get_user_by_id(db, userid)
    response = {
        "success": True,
        "message": "User fetched Successfully",
        "data": user["data"],
        "cached": user["cached"]
    }
    return response


@router.get("/users", response_model=UserListOut)
async def get_all_users( request: Request,db:AsyncSession = Depends(get_db), options:QueryOptionsDto = Depends() ):
    userList = await service.get_all_users(db, request, options)
    return {
        "success": True,
        "message": "Users Fetched Successfully",
        "data": userList["data"]["data"],
        "meta": userList["data"]["meta"],
        "cached": userList["cached"]
    }
