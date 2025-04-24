from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from db.database import get_db
from sqlalchemy.orm import Session
import jwt

class ActiveUserMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            if request.url.path.startswith("/protected") or request.url.path.startswith("/users"):
                token = request.headers.get("Authorization")
                if token and token.startswith("Bearer "):
                    token = token.split(" ")[1]
                    db: Session = next(get_db())
                    payload = jwt.decode(token, options={"verify_signature": False})
                    email = payload.get("sub")

                    from models.user import User
                    user = db.query(User).filter(User.email == email).first()
                    if user and user.status is False:
                        return JSONResponse(status_code=403, content={"message": "Usuário inativo"})
            response = await call_next(request)
            return response
        except Exception as e:
            return JSONResponse(status_code=401, content={"message": "Erro de autenticação"})
