from models.movie import Movie as moviemodel

class MovieService():
    
    def __init__(self, db) -> None:
        self.db = db
        
    def get_movies(self):
        result = self.db.query(moviemodel).all()
        return result
    
    def get_movie(self, id):
        result = self.db.query(moviemodel).filter(moviemodel.id == id).first()
        return result
    
    def get_movie_by_category(self, category):
        result = self.db.query(moviemodel).filter(moviemodel.category == category).all()
        return result