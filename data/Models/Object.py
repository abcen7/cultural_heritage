import datetime
from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey, orm
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
    on_map = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    category = orm.relation("Category")
    type = orm.relation("Type")

    # def __init__(self, name: str, surname: str, age: int, password: str, email: str):
    #     self.name = name
    #     self.surname = surname
    #     self.age = age
    #     self.email = email
    #     self._set_password(password)

    def __repr__(self):
        return f'{self.type.title} ; {self.category.title}'
