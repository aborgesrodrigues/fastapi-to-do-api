

import os
import time
from http import HTTPStatus

import jwt
from fastapi import Request
from fastapi.responses import JSONResponse
from jwt import ExpiredSignatureError, InvalidTokenError
from prometheus_client import Counter, Histogram

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

PUBLIC_PATHS = {
    "/token",
    "/login",
    "/docs",
    "/redoc",
    "/openapi.json",
}

def unauthorized(detail: str) -> JSONResponse:
    return JSONResponse(
        status_code=HTTPStatus.UNAUTHORIZED,
        content={"detail": detail},
        headers={"WWW-Authenticate": "Bearer"},
    )


async def jwt_auth_middleware(request: Request, call_next):
    # Don't refequest token for public paths
    if request.method == "OPTIONS" or request.url.path in PUBLIC_PATHS:
        return await call_next(request)
 
    # 1. header exists
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return unauthorized("Missing token")
 
    # 2. correct format "Bearer <token>"?
    scheme, _, token = auth_header.partition(" ")
    if scheme.lower() != "bearer" or not token:
        return unauthorized("Invalid Authorization header valid")
 
    # 3. valid (signature + expiration)?
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
            options={"require": ["exp", "type", "sub"]},  # required clams
        )
    except ExpiredSignatureError:
        return unauthorized("Expired token")
    except InvalidTokenError:
        return unauthorized("Invalid token")
 
    # 4. set token to the routes
    request.state.user = payload["sub"]
    request.state.token_payload = payload
 
    return await call_next(request)


REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "Latência das requisições HTTP em segundos",
    ["method", "path", "status_code"],
    buckets=(0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5, 10),
)

REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total de requisições HTTP",
    ["method", "path", "status_code"],
)

async def prometheus_middleware(request: Request, call_next):
    start = time.perf_counter()
    status_code = 500  # caso ocorra exceção não tratada
    try:
        response = await call_next(request)
        status_code = response.status_code
        return response
    finally:
        elapsed = time.perf_counter() - start
        route = request.scope.get("route")
        path = route.path if route else "unmatched"

        labels = {"method": request.method, "path": path, "status_code": status_code}
        REQUEST_LATENCY.labels(**labels).observe(elapsed)
        REQUEST_COUNT.labels(**labels).inc()
