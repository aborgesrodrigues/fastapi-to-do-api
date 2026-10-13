

import os
import time

from fastapi import Request
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
