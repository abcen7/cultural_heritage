import os
from functools import wraps

from cryptography.fernet import InvalidToken
from flask import request, jsonify

from Classes.Token import Token


def load_environment_variable() -> None:
    """This function loads environment variable from .env file"""
    from os import path
    from dotenv import load_dotenv  # library for work with .env files
    basedir = path.abspath(path.dirname(__file__))  # find absolute path
    load_dotenv(path.join(basedir, r"../.env"))  # add .env to path and load .env file


def get_models_path(abs_path: str) -> str:
    """Get path for import Models"""
    elements = abs_path.split("\\")
    separator: str = ''
    if len(elements) < 2 or elements[-2] != "data":
        elements.extend(("data", "Models"))
    elif elements[-1] != "Models":
        elements.append("Models")
    if os.name == 'nt':
        separator: str = '\\'
    elif os.name == 'posix':
        separator: str = '/'
    return separator.join(el for el in elements)


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        if 'x-access-tokens' not in request.headers:
            return jsonify({'message': 'valid token is missing'})
        token = request.headers['x-access-tokens']
        try:
            if not Token().is_token_valid(token):
                return jsonify({'message': 'token is invalid'})
        except InvalidToken:
            return jsonify({'message': 'token is invalid'})
        return f(*args, **kwargs)
    return decorator
