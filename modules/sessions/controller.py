from fastapi import APIRouter, Depends


session_route = APIRouter()


@session_route.get("/sessions")
async def get_all_sessions():
    ...
@session_route.get("/sessions/{sessionId}")
async def get_single_sessions():
    ...
@session_route.get("/sessions/user/{userId}")
async def get_userbase_sessions():
    ...
