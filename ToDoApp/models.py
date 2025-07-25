from database import Base

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey


class User(Base):

    __tablename__ = "usertable"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String)



class Todo(Base):

    # In DBMS, table contains columns and rows, The rows are also called as records
    __tablename__ = "todolist"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    completed = Column(Boolean, default=False)
    owner = Column(Integer, ForeignKey("usertable.id"))
