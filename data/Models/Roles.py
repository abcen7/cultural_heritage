from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from werkzeug.security import generate_password_hash, check_password_hash

from Classes.SqlAlchemyDatabase import SqlAlchemyBase
from flask_login import UserMixin


class Roles(SqlAlchemyBase, UserMixin):
    __tablename__ = "roles"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    role = Column(String, nullable=True)



