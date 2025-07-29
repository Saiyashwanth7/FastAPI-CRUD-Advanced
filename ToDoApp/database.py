from sqlalchemy import (
    create_engine,
)  # create_engine is creates a connection between the users and the database

from sqlalchemy.orm import (
    sessionmaker,
)  # sessionmaker will create a local session where all the fastapi endpoint queries are stored. This sessionLocal will be temporary and will be refreshed each time

from sqlalchemy.ext.declarative import declarative_base

SQL_ALCHEMY_DATABASE = "postgresql://postgres:1913101243@localhost:5432/ToDoApplicationDatabase"  # This will create the todos database in this folder using sqlite

engine = create_engine(SQL_ALCHEMY_DATABASE)

sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
  # This declarative base will maintain the ORM in the database, THis base is where all the ORM models (Tables) will be inherited from
