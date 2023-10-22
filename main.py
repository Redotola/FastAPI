from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from config.database import engine, Base
from middleware.error_handler import ErrorHandler
from routers.movie import movie_router
from routers.user import user_router

#information of the app
app = FastAPI()
app.title = "Mi aplicacion con FastAPI"
app.version = "0.0.1"

app.add_middleware(ErrorHandler)
app.include_router(movie_router)
app.include_router(user_router)

Base.metadata.create_all(bind=engine)

#home page
@app.get('/', tags = ['home'])
def message():
    return HTMLResponse('<h1>Hello World</h1>')



