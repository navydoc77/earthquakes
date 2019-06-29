from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy import text
from dotenv import load_dotenv
import os
import pymysql

def db_conn():
    # Parse the .env file to set DB environment variables.
    load_dotenv()

    pymysql.install_as_MySQLdb()

    # # Database Connection
    username = os.getenv("DATABASE_USERNAME")
    password = os.getenv("DATABASE_PASSWORD")
    host = os.getenv("DATABASE_HOST")
    port = os.getenv("DATABASE_PORT")
    database = os.getenv("DATABASE_NAME")
    engine = create_engine(f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}")

    return engine
