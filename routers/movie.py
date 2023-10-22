from fastapi import APIRouter, Depends, Path, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from config.database import Session
from models.movie import Movie as MovieModel
#from starlette.requests import Request
from fastapi.encoders import jsonable_encoder
from middleware.jwt_bearer import JWTBearer

movie_router = APIRouter()

#schema class Movie with BaseModel and Field validations
class Movie(BaseModel):
    id: Optional[int] = None 
    title: str = Field(min_length = 5 ,max_length=15)
    overview: str = Field(min_length = 15 ,max_length=60)
    year: int = Field(default = 2023, le=2023)
    rating: float = Field(ge = 0, le = 10)
    category: str = Field(min_length = 5, max_length = 15)
    
    #default model
    class Config: 
        json_schema_extra = {
            "exameple": {
                "id" : 1,
                "title" : "Pelicula",
                "overview" : "Descripcion de la pelicula",
                "year" : 2023,
                "rating" : 9.8,
                "category" : "Accion"
            }
        }

# method to obtain all the movies
@movie_router.get('/movies', tags = ['movies'], response_model=List[Movie], status_code = 200, dependencies = [Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    db = Session()
    result = db.query(MovieModel).all()
    return JSONResponse(status_code = 200,content = jsonable_encoder(result))

#method to obtain movies with an specific id
@movie_router.get('/movies/{id}', tags = ['movies'], response_model=Movie) #Parameter mode
def get_movie_by_id(id: int = Path(ge=1, le = 2002)) -> Movie:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        return JSONResponse(status_code=404, content = {"message": "No encontrado"})
    return JSONResponse(status_code = 200, content= jsonable_encoder(result))


#method to get movies with a specific category
@movie_router.get('/movies/', tags = ['movies'], response_model = List[Movie]) #Query mode
def get_movies_by_category(category: str = Query(min_length = 5, max_length = 15)) -> List[Movie]:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.category == category).all()
    return JSONResponse(status_code = 200,content = jsonable_encoder(result))

#method to create a new movie
@movie_router.post('/movies', tags = ['movies'], response_model = dict,status_code = 201)
def create_movie(movie: Movie) -> dict:
    db = Session()
    new_movie = MovieModel(**movie.model_dump())
    db.add(new_movie) # add new movie t
    db.commit() #update the changes in the database
    return JSONResponse(status_code = 201 ,content={"message": "Se ha registrado la pelicula correctamente"})

#method to update information from a specific movie by id
@movie_router.put('/movies/{id}', tags = ['movies'], response_model = dict, status_code = 200)
def update_movie(id : int, movie: Movie) -> dict:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        return JSONResponse(status_code = 404, content = {"message": "No encontrado"})
    result.title = movie.title
    result.category = movie.category
    result.overview = movie.overview
    result.rating = movie.rating
    result.year = movie.year
    db.commit()
    return JSONResponse(status_code = 200, content = {'mesage': "Se ha actualizado correctamente la informacion de la pelicula"})

#method to delete a movie with id
@movie_router.delete('/movies/{id}', tags = ['movies'], response_model = dict, status_code = 200)
def delete_movie(id: int) -> dict:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        return JSONResponse(status_code = 404, content = {"message":"No se encontro"})
    db.delete(result)
    db.commit()      
    return JSONResponse(status_code = 200, content = {"mesage": "Se ha eliminado correctamente la pelicula"})

