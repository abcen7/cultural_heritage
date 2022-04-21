import datetime

import sqlalchemy.types
from sqlalchemy import Column, String, Integer, DateTime, Text, Boolean, ForeignKey, orm
from Classes.SqlAlchemyDatabase import SqlAlchemyBase


class Object(SqlAlchemyBase):
    __tablename__ = "objects"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    register_number = Column(Integer, unique=True)
    region = Column(String, nullable=True)
    full_address = Column(String, nullable=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    type_id = Column(Integer, ForeignKey("types.id"), nullable=False)
    belonging_to_unesco = Column(Boolean, nullable=False)
    especially_valuable = Column(Boolean, nullable=False)
    on_map = Column(String, nullable=True)
    files = Column(Text, nullable=True)


    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)

    category = orm.relation("Category")
    type = orm.relation("Type")
    comment = orm.relationship("Comment", uselist=False, back_populates="object")

    def __repr__(self):
        return f"<Object id: {self.id}, title: {self.title}>"
