from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from fastapi.responses import JSONResponse
from core.security import verify_access_token


PUBLIC_EXACT = {
    "/static",
    "/favicon.ico",
}

EXCLUDED_PATHS = [
    "/",
    "/health-check",
    "/auth/login",
    "/forgot-password",
    "/docs",
    "/openapi.json",
     
]

class SecurityMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):

        # ✅ Skip public routes
        if any(request.url.path.startswith(p) for p in PUBLIC_EXACT):
            return await call_next(request)
        
        if request.url.path in EXCLUDED_PATHS:
            return await call_next(request)


        # ✅ Check Authorization
        auth = request.headers.get("authorization")
        if not auth or not auth.startswith("Bearer"):
            return JSONResponse(
                status_code=401,
                content={"success": False, "message": "Authorization required"}
            )
            
        token = auth.split(" ")[1]
        print("only token✅✅✅", token)

        jwt_verification = verify_access_token(token)
        print("this is the result o fjwt_verification: ", jwt_verification)
        
        if not jwt_verification:
            return JSONResponse(
                status_code=401,
                content={"success": False, "message": "UnAuthorized please relogin"}
            )
            
        request.state.userId = jwt_verification.get("userId")
        # ✅ Check device headers
        required_headers = [
            "x-fingerprint",
            "x-device-name",
            "x-device-type",
            "x-os",
            "x-browser",
            "x-client-id",
            "x-source",
            "x-ip",
            "x-userAgent"
            
            
        ]

        # for h in required_headers:
        #     if not request.headers.get(h):
        #         return JSONResponse(
        #             status_code=400,
        #             content={"success": False, "message": f"Missing header: {h}"}
        #         )

        return await call_next(request)