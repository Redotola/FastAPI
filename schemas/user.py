from pydantic import BaseModel

#class User 
class User(BaseModel):
    email: str
    password: str