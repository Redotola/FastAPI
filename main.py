from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from jwt_manager import create_token
from config.database import engine, Base
#from starlette.requests import Request
from middleware.error_handler import ErrorHandler
from routers.movie import movie_router

#information of the app
app = FastAPI()
app.title = "Mi aplicacion con FastAPI"
app.version = "0.0.1"

app.add_middleware(ErrorHandler)
app.include_router(movie_router)

Base.metadata.create_all(bind=engine)

#class User 
class User(BaseModel):
    email: str
    password: str

#dictionary of movies with examples
movies = [
    {
        "id": 1,
        "title": "Star Wars",
        "overview": "En una galaxia muy lejana se iniciaba una guerra que definiria el futuro de el universo",
        "year": 1977,
        "rating": 7.8,
        "category": "Ciencia Ficcion"
    },
    {
        "id": 2,
        "title": "Star Wars",
        "overview": "En una galaxia muy lejana se iniciaba una guerra que definiria el futuro de el universo",
        "year": 1977,
        "rating": 7.8,
        "category": "Accion"
    }
]

#home page
@app.get('/', tags = ['home'])
def message():
    return HTMLResponse('<h1>Hello World</h1>')

#method to login user with password and email and create a token for the session
@app.post('/login', tags = ['auth'])
def login(user: User):
    if user.email == "user" and user.password == "password":
        token: str = create_token(user.model_dump())    
        return JSONResponse(status_code = 200, content = token)
    return JSONResponse(status_code = 404)

