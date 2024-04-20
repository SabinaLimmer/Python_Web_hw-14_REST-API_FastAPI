from ipaddress import ip_address
from typing import Callable
from fastapi.responses import JSONResponse
import redis.asyncio as redis
from fastapi_limiter import FastAPILimiter
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware

from src.routes import contacts, auth, users
from src.conf.config import settings


ORIGINS = [
    settings.origins_url
    ]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(contacts.router, prefix='/api')
app.include_router(auth.router, prefix='/api')
app.include_router(users.router, prefix='/api')

@app.on_event("startup")
async def startup():
    """
    Function to run on application startup to initialize the connection to Redis and FastAPILimiter.
    """
    r = await redis.Redis(host=settings.redis_host, port=settings.redis_port, db=0, encoding="utf-8",
                          decode_responses=True)
    await FastAPILimiter.init(r)