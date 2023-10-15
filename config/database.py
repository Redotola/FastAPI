import os #import os that allow us to use the different files and folders of our system
from sqlalchemy import create_engine #import sqlalchemy to create the engine
from sqlalchemy.orm.session import sessionmaker #import sessionmaker to create the session
from sqlalchemy.ext.declarative import declarative_base #import declarative_base to create the declarative

sqlite_file_name = "../database.sqlite" #name of the sqlite database
base_dir = os.path.dirname(os.path.realpath(__file__)) #actual base directory

database_url = f"sqlite:///{os.path.join(base_dir, sqlite_file_name)}" #actual database url path

engine = create_engine(database_url, echo = True) #creation of the engine object

Session = sessionmaker(bind = engine) #create a session object

Base = declarative_base() #create a base class instance