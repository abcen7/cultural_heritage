import datetime
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from Classes.SqlAlchemyDatabase import SqlAlchemyBase


class Category(SqlAlchemyBase):
    __tablename__ = "categories"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)


    def __repr__(self):
        return '<Type {}>'.format(self.body)