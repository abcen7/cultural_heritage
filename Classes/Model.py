from Classes.SqlAlchemyDatabase import SqlAlchemyDatabase

import importlib

from flask_restful import Resource, abort
from sqlalchemy.orm.session import Session


class Model(Resource):
    def __init__(self, child_class_name: str):
        self.db = SqlAlchemyDatabase()
        self._child_class_name = child_class_name
        self.Model = getattr(importlib.import_module("Data.Models." + child_class_name), child_class_name)

    def get_object(self, id: int, session: Session):
        """Retrieves an object in the session that was passed by id"""
        try:
            obj = session.query(self.Model).get(id)
            if obj is None:
                raise IndexError
            return obj
        except IndexError:
            session.rollback()
            abort(404, message=f"{self._child_class_name} {id} not found")
        except Exception as ex:
            session.rollback()
            print(type(ex))
            print(ex)
