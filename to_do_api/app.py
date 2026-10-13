import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware

from to_do_api.dao.dao import DAO
from to_do_api.middlewares import jwt_auth_middleware

__LOG_FMT = "{\"time\": \"%(asctime)s\", \"name\": \"[%(name)s]\", \"filename\": \"[%(filename)s]\", \"lineno\": \"[%(lineno)s]\", \"levelname\": \"%(levelname)s\", \"message\": \"%(message)s\"}"

logging.basicConfig(level=logging.INFO, format=__LOG_FMT)

@asynccontextmanager
async def lifespan(app: FastAPI):
    DAO.init_pool()    # startup: create pool of database connections
    yield
    DAO.close_pool()   # shutdown: close all the connections


app = FastAPI(lifespan=lifespan)

# append the routes
from to_do_api.exception_handlers import register_exception_handlers
from to_do_api.handlers.base import base_routes
from to_do_api.handlers.task import task_routes
from to_do_api.handlers.user import user_routes

app.include_router(user_routes)
app.include_router(task_routes)
app.include_router(base_routes)

app.add_middleware(BaseHTTPMiddleware, dispatch=jwt_auth_middleware)

register_exception_handlers(app)
