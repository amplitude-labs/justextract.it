from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from verify import verifyKey

class VerifyKeyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path.startswith("/api/protected"):
            authorization: str = request.headers.get("Authorization")
            
            if not authorization or not authorization.startswith("Bearer "):
                return JSONResponse(
                    status_code=400, 
                    content={"detail": "Authorization header missing or invalid"}
                )
            
            token = authorization[len("Bearer "):] 
            
            result = verifyKey(token)
            if not result.get("valid", False):
                return JSONResponse(
                    status_code=401, 
                    content={"detail": "UNAUTHORIZED"}
                )
        
        response = await call_next(request)
        return response
