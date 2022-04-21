from Classes.ServerBuilder import ServerBuilder

from os import environ

from cryptography.fernet import Fernet


class Token:
    TIME_EXPIRATION: int = 0  # Never expires

    def __init__(self):
        self._secret_key: str = environ.get("SECRET_KEY")
        self._encryption = Fernet(b'CtJTNc5Ei-DPioGiaNYDJFsrpuaD8hfWOZrUG9pWhcA=')
        self._server_host = ServerBuilder().get_server()

    def is_token_valid(self, encrypted_token: str) -> bool:
        # Decrypting encrypted token
        decrypted_token = self._encryption.decrypt(bytes(encrypted_token.encode("utf-8")))
        data = decrypted_token.decode("utf-8").split('.')
        # check user
        from Classes.SqlAlchemyDatabase import SqlAlchemyDatabase
        from Data.Models.User import User
        database = SqlAlchemyDatabase()
        session = database.create_session()
        user = session.query(User).get(int(data[1]))
        if user is None:
            return False
        # Checking valid secret key, valid user id and expiration time
        if data[0] == str(self._secret_key) and int(data[2]) == self.TIME_EXPIRATION:
            return True
        else:
            return False

    def get_token(self, user_id: int) -> str:
        data = {
            "key": self._secret_key,
            "id": str(user_id),
            "expiration": str(self.TIME_EXPIRATION)
        }
        token = f"{data['key']}.{data['id']}.{data['expiration']}"
        encrypted_token = self._encryption.encrypt(bytes(token.encode("utf-8"))).decode("utf-8")
        return encrypted_token
