from fastapi import FastAPI, Body
from fastapi.responses import HTMLResponse

app = FastAPI()
app.title = "Mi aplicacion con FastAPI"
app.version = "0.0.1"

movies = [
    {
        "id": 1,
        "title": "Star Wars",
        "overview": "En una galaxia muy lejana se iniciaba una guerra que definiria el futuro de el universo",
        "year": "1977",
        "rating": 7.8,
        "categoria": "Ciencia Ficcion"
    },
    {
        "id": 2,
        "title": "Star Wars",
        "overview": "En una galaxia muy lejana se iniciaba una guerra que definiria el futuro de el universo",
        "year": "1977",
        "rating": 7.8,
        "categoria": "Ciencia Ficcion"
    }
]

@app.get("/", tags = ['home'])
def message():
    return HTMLResponse('<h1>Hello World</h1>')

@app.get("/movies", tags = ['movies'])
def get_movies():
    return movies

@app.get('/movies/{id}', tags = ['movies']) #Parameter mode
def get_movie_by_id(id: int):
    for item in movies:
        if item["id"] == id:
            return item
    return []

@app.get("/movies/", tags = ["movies"]) #Query mode
def get_movies_by_category(category: str):
            return [item for item in movies if category == category]
        
@app.post("/movies", tags = ['movies'])
def create_movie(id: int = Body(), title: str = Body(), overview: str = Body(), year: int = Body(), rating: float = Body(), category: str = Body()):
    movies.append({
        "id" : id,
        "title" : title,
        "overview" : overview,
        "year" : year,
        "rating" : rating,
        "category" : category
    })
    return movies

 