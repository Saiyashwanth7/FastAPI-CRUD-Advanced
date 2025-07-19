from database import Base

from sqlalchemy import Column, Integer, String, Boolean


class Todo:

    # In DBMS, table contains columns and rows, The rows are also called as records
    __tablename__ = "Todo list"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    completed = Column(Boolean, default=False)
