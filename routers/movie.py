from fastapi import APIRouter, Depends, Path, Query
from fastapi.responses import JSONResponse
from typing import List
from config.database import Session
from models.movie import Movie as MovieModel
#from starlette.requests import Request
from fastapi.encoders import jsonable_encoder
from middleware.jwt_bearer import JWTBearer
from services.movie import MovieService
from schemas.movie import Movie

movie_router = APIRouter()


# method to obtain all the movies
@movie_router.get('/movies', tags = ['movies'], response_model=List[Movie], status_code = 200, dependencies = [Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    db = Session()
    result = MovieService(db).get_movies()
    return JSONResponse(status_code = 200,content = jsonable_encoder(result))

#method to obtain movies with an specific id
@movie_router.get('/movies/{id}', tags = ['movies'], response_model=Movie) #Parameter mode
def get_movie_by_id(id: int = Path(ge=1, le = 2002)) -> Movie:
    db = Session()
    result = MovieService(db).get_movie(id)
    if not result:
        return JSONResponse(status_code=404, content = {"message": "No encontrado"})
    return JSONResponse(status_code = 200, content= jsonable_encoder(result))


#method to get movies with a specific category
@movie_router.get('/movies/', tags = ['movies'], response_model = List[Movie]) #Query mode
def get_movies_by_category(category: str = Query(min_length = 5, max_length = 15)) -> List[Movie]:
    db = Session()
    result = MovieService(db).get_movie_by_category(category)
    return JSONResponse(status_code = 200,content = jsonable_encoder(result))

#method to create a new movie
@movie_router.post('/movies', tags = ['movies'], response_model = dict,status_code = 201)
def create_movie(movie: Movie) -> dict:
    db = Session()
    MovieService(db).create_movie(movie)
    return JSONResponse(status_code = 201 ,content={"message": "Se ha registrado la pelicula correctamente"})

#method to update information from a specific movie by id
@movie_router.put('/movies/{id}', tags = ['movies'], response_model = dict, status_code = 200)
def update_movie(id : int, movie: Movie) -> dict:
    db = Session()
    result = MovieService(db).get_movie(id)
    if not result:
        return JSONResponse(status_code = 404, content = {"message": "No encontrado"})
    MovieService(db).update_movie(id, movie)
    return JSONResponse(status_code = 200, content = {'mesage': "Se ha actualizado correctamente la informacion de la pelicula"})

#method to delete a movie with id
@movie_router.delete('/movies/{id}', tags = ['movies'], response_model = dict, status_code = 200)
def delete_movie(id: int) -> dict:
    db = Session()
    result = MovieService.get_movie(id)
    if not result:
        return JSONResponse(status_code = 404, content = {"message":"No se encontro"})
    MovieService(db).delete_movie(id)
    return JSONResponse(status_code = 200, content = {"mesage": "Se ha eliminado correctamente la pelicula"})

