from fastapi import FastAPI, Body, Path, Query
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List

#class Movie with BaseModel and Field validations
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
                "category" : "Accion",  
            }
        }

#information of the app
app = FastAPI()
app.title = "Mi aplicacion con FastAPI"
app.version = "0.0.1"

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

# method to obtain all the movies
@app.get('/movies', tags = ['movies'], response_model=List[Movie], status_code=200)
def get_movies() -> List[Movie]:
    return JSONResponse(status_code = 200,content = movies)

#method to obtain movies with an specific id
@app.get('/movies/{id}', tags = ['movies'], response_model=Movie) #Parameter mode
def get_movie_by_id(id: int = Path(ge=1, le = 2002)) -> Movie:
    for item in movies:
        if item["id"] == id:
            return JSONResponse(content=item)
    return JSONResponse(status_code = 404, content=[])


#method to get movies with a specific category
@app.get('/movies/', tags = ['movies'], response_model = List[Movie]) #Query mode
def get_movies_by_category(category: str = Query(min_length = 5, max_length = 15)) -> List[Movie]:
    data = [item for item in movies if item["category"] == category]
    return JSONResponse(content=data)

#method to create a new movie
@app.post('/movies', tags = ['movies'], response_model = dict,status_code = 201)
def create_movie(movie: Movie) -> dict:
    movies.append(movie)
    return JSONResponse(status_code = 201 ,content={"message": "Se ha registrado la pelicula correctamente"})

#method to update information from a specific movie by id
@app.put('/movies/{id}', tags = ['movies'], response_model = dict, status_code = 200)
def update_movie(id : int, movie: Movie) -> dict:
    for item in movies:
        if item["id"] == id:
            item["title"] = movie.title
            item["overview"] = movie.overview
            item["year"] = movie.year
            item["rating"] = movie.rating
            item["category"] = movie.category
    return JSONResponse(status_code = 200, content = {'mesage': "Se ha actualizado correctamente la informacion de la pelicula"})

#method to delete a movie with id
@app.delete('/movies/{id}', tags = ['movies'], response_model = dict, status_code = 200)
def delete_movie(id: int) -> dict:
    for item in movies:
        if item["id"] == id:
            movies.remove(item)
            return JSONResponse(status_code = 200, content={"mesage": "Se ha eliminado correctamente la pelicula"})

