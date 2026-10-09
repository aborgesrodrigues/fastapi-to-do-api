import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from to_do_api.dao.dao import DAO

__LOG_FMT = "{\"time\": \"%(asctime)s\", \"name\": \"[%(name)s]\", \"filename\": \"[%(filename)s]\", \"lineno\": \"[%(lineno)s]\", \"levelname\": \"%(levelname)s\", \"message\": \"%(message)s\"}"

@asynccontextmanager
async def lifespan(app: FastAPI):
    DAO.init_pool()    # startup: create pool of database connections
    yield
    DAO.close_pool()   # shutdown: close all the connections


app = FastAPI(lifespan=lifespan)

# append the routes
from to_do_api.exception_handlers import register_exception_handlers
from to_do_api.handlers.user import user_routes

app.include_router(user_routes)
register_exception_handlers(app)

logging.basicConfig(level=logging.INFO, format=__LOG_FMT)
