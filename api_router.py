from fastapi import APIRouter
from modules.users.controller import router as user_routes
from modules.auth.controller import auth_router

api_router  = APIRouter()

api_router.include_router(user_routes)
api_router.include_router(auth_router)
