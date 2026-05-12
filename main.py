from fastapi import FastAPI, Body, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from core.redis import check_redis_connection
from core.rabbitmq import RabbitMQ
from core.redis import close_redis
import uvicorn
import models
from api_router import api_router

from core.database import Base, engine

from fastapi.middleware.cors import CORSMiddleware

from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from core.exceptions.app_exception import AppException
from core.exceptions.handlers import (
    app_exception_handler,
    validation_exception_handler,
    sqlalchemy_exception_handler,
    integrity_exception_handler,
    global_exception_handler
)
from middlware.auth_middleware import SecurityMiddleware

app = FastAPI()
origins = [
    "http://localhost:3000",   # React
    "http://127.0.0.1:3000",
    "http://localhost:5173",   # Vite
    "https://yourdomain.com",  # Production frontend
]
app.include_router(api_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)
app.add_exception_handler(IntegrityError, integrity_exception_handler)
app.add_exception_handler(Exception, global_exception_handler)
app.add_middleware(SecurityMiddleware)


rabbitmq = RabbitMQ()
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await check_redis_connection()
    await rabbitmq.connect()
    


@app.on_event("shutdown")
async def shutdown():
    await rabbitmq.close()
    await close_redis()

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates directory
templates = Jinja2Templates(directory="templates")



@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse(
        name = "index.html",   # template name
        request = request
    )

@app.get("/health-check")
async def health_check():
    return {
        "status": True,
        "message": "health check request received by Backend"
    }




if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)