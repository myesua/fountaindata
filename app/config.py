import os
from dotenv import load_dotenv

load_dotenv() 

DATABASE_URL = os.environ.get(
    "DATABASE_URL", 
    "postgres://postgres:password@localhost:5432/fountain_db_default" 
)