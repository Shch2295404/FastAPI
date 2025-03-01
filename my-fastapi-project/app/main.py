from contextlib import asynccontextmanager

from fastapi import FastAPI, logger
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache

from redis import asyncio as aioredis

from app.config import settings
from app.users.router import router as router_users
from app.bookings.router import router as router_bookings
from app.hotels.router import router as router_hotels
from app.hotels.rooms.router import router as router_rooms

from app.pages.router import router as router_pages
from app.images.router import router as router_images


app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(router_users)
app.include_router(router_hotels)
app.include_router(router_rooms)
app.include_router(router_bookings)

app.include_router(router_pages)
app.include_router(router_images)


# Подключение CORS, чтобы запросы к API могли приходить из браузера 
origins = [
    # 3000 - порт, на котором работает фронтенд на React.js 
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", 
                   "Access-Control-Allow-Origin",
                   "Authorization"],
)


# @app.on_event("startup")  # <-- данный декоратор прогоняет код перед запуском FastAPI
# def startup():
#     redis = aioredis.from_url("redis://localhost:6379", encoding="utf-8", decode_responses=True)
#     FastAPICache.init(RedisBackend(redis), prefix="cache")


# @app.on_event("shutdown")  # <-- данный декоратор прогоняет код после завершения программы
# def shutdown_event():
#     pass

# Замена устаревших @app.on_event("startup") и @app.on_event("shutdown")
# в единую функцию lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
    # при запуске
    redis = aioredis.from_url(
        f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
        encoding="utf8",
        decode_responses=True,
    )
    FastAPICache.init(RedisBackend(redis), prefix="cache")
    yield
    # при выключении

# app = FastAPI(lifespan=lifespan)
