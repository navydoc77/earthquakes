import os

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine


# Database Connection
dialect = os.getenv("DATABASE_DIALECT")
username = os.getenv("DATABASE_USERNAME")
password = os.getenv("DATABASE_PASSWORD")
host = os.getenv("DATABASE_HOST")
port = os.getenv("DATABASE_PORT")
database = os.getenv("DATABASE_NAME")

# Format:
#
# `<Dialect>://<Username>:<Password>@<Host Address>:<Port>/<Database>`
# Using f-string notation: https://docs.python.org/3/reference/lexical_analysis.html#f-strings
#
connection = f"{dialect}://{username}:{password}@{host}:{port}/{database}"

# Create an engine to the database
engine = create_engine(connection, echo=False)

# Reflect an existing database into a new model
Base = automap_base()

# Reflect the tables
Base.prepare(engine, reflect=True)

warnings = Base.classes.warnings

# Create a session
session = Session(bind=engine)


if __name__ == "__main__":
    print("Available automap classes:")
    print(Base.classes.keys())
