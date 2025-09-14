# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.ext.declarative import declarative_base

# URL_DATABASE = "mysql+pymysql://root:36SM%23Ro%40groot24@localhost:3306/blogapplication"

# engine = create_engine(URL_DATABASE)

# SessionLocal = sessionmaker(autoflush=False, autocommit = False, bind=engine)

# Base=declarative_base()


import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
from urllib.parse import quote_plus

# Load environment variables from a .env file
load_dotenv()

# --- Load credentials securely from environment variables ---
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "blogapplication")

# --- URL-encode the password to handle special characters ---
encoded_password = quote_plus(DB_PASSWORD)

URL_DATABASE = f"mysql+pymysql://{DB_USER}:{encoded_password}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(URL_DATABASE)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

