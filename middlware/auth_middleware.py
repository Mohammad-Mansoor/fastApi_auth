from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from fastapi.responses import JSONResponse

EXCLUDED_PATHS = [
    "/",
    "/login",
    "/forgot-password",
    "/docs",
    "/openapi.json"
]

class SecurityMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):

        # ✅ Skip public routes
        if any(request.url.path.startswith(p) for p in EXCLUDED_PATHS):
            return await call_next(request)

        # ✅ Check Authorization
        auth = request.headers.get("authorization")
        if not auth:
            return JSONResponse(
                status_code=401,
                content={"success": False, "message": "Authorization required"}
            )

        # ✅ Check device headers
        required_headers = [
            "x-fingerprint",
            "x-device-name",
            "x-device-type",
            "x-os",
            "x-browser",
            "x-client-id"
        ]

        for h in required_headers:
            if not request.headers.get(h):
                return JSONResponse(
                    status_code=400,
                    content={"success": False, "message": f"Missing header: {h}"}
                )

        return await call_next(request)