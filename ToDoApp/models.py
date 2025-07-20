from database import Base

from sqlalchemy import Column, Integer, String, Boolean


class Todo(Base):

    # In DBMS, table contains columns and rows, The rows are also called as records
    __tablename__ = "todolist"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    completed = Column(Boolean, default=False)
