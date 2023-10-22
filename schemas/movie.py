#schema class Movie with BaseModel and Field validations
from typing import Optional
from pydantic import BaseModel, Field


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