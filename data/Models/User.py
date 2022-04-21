import datetime

from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import orm
from Classes.SqlAlchemyDatabase import SqlAlchemyBase
from flask_login import UserMixin


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = "users"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=True)
    surname = Column(String, nullable=True)
    age = Column(Integer, nullable=True)
    email = Column(String, unique=True, nullable=True)
    hashed_password = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    role_id = Column(Integer, ForeignKey("roles.id"), default=1)
    role = orm.relation('Roles')

    def __init__(self, name: str, surname: str, age: int, password: str, email: str):
        self.name = name
        self.surname = surname
        self.age = age
        self.email = email
        self._set_password(password)

    def __repr__(self):
        return f"{self.name} {self.surname}"

    def _set_password(self, password: str) -> None:
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.hashed_password, password)

    def is_admin(self):
        return self.role_id == 2