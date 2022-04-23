import sqlalchemy

from data.Functions import load_environment_variable, get_models_path

import importlib
import os

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

SqlAlchemyBase = declarative_base()
_session = None


class SqlAlchemyDatabase:
    def __init__(self, database_file: str = r"../../db/cultural_heritage.db", create=False, delete=False):
        """
        Init database
        :param create: if true create all Models
        :param delete: if true delete all Models
        """
        self._global_init(database_file, create, delete)

    @staticmethod
    def _global_init(database_file: str, create: bool, delete: bool) -> None:
        global _session
        if _session:  # if session config created do nothing
            return None
        load_environment_variable()
        abs_path = os.path.abspath(os.curdir)
        os.chdir(get_models_path(abs_path))

        print(database_file)
        print(os.path.abspath(database_file))

        if not database_file or not database_file.strip():
            raise Exception("Необходимо указать файл базы данных.")

        connection = f'sqlite:///{os.path.abspath(database_file.strip())}?check_same_thread=False'
        print(f"LOG: Подключение к базе данных по адресу {connection}")
        engine = sqlalchemy.create_engine(connection, echo=False)
        _session = sessionmaker(bind=engine)  # create session config

        files = [el.split('.')[0] for el in os.listdir() if el.endswith(".py")]  # get all files with Models
        os.chdir(r"../../")
        for module in files:
            importlib.import_module("data.Models." + module)  # import them in current file=
        if delete:
            SqlAlchemyBase.metadata.drop_all(engine)  # removing Data from database
        if create:
            print("LOG: creating the data to db")
            SqlAlchemyBase.metadata.create_all(engine)  # adding Data to database

    @staticmethod
    def create_session() -> Session:
        global _session
        return _session()  # return Session object from session config
