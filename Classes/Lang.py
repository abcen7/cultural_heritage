import json


# TODO: нормально доработать lang и сделать абстракцию от символов, сделать так, чтобы нужно было format'om подменять
#  это
from typing import List


class Lang:

    def __init__(self, lang: str):
        self.lang: str = lang

    def get(self, param: str, args: List[str] = []) -> str:
        data = self._get_data()
        if data:
            return data[param].format(*[arg.lower() for arg in args])
        else:
            return ""

    def _get_data(self) -> list:
        try:
            with open(f"data/Lang/{self.lang}-{self.lang.upper()}.json", mode='r') as file:
                data = json.load(file)
                if data:
                    return data
        except FileNotFoundError:
            print(f"<LangNotFoundError> File Data/Lang/{self.lang}.json doesn't exist")
