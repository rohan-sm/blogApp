from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

URL_DATABASE = "mysql+pymysql://root:36SM%23Ro%40groot24@localhost:3306/blogapplication"

engine = create_engine(URL_DATABASE)

SessionLocal = sessionmaker(autoflush=False, autocommit = False, bind=engine)

Base=declarative_base()