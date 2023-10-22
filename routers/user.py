from fastapi.responses import JSONResponse
from jwt_manager import create_token
from pydantic import BaseModel
from fastapi import APIRouter
from schemas.user import User

user_router = APIRouter()
    
#method to login user with password and email and create a token for the session
@user_router.post('/login', tags = ['auth'])
def login(user: User):
    if user.email == "user" and user.password == "password":
        token: str = create_token(user.model_dump())    
        return JSONResponse(status_code = 200, content = token)
    return JSONResponse(status_code = 404)
