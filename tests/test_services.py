from settings import OPEN_XLS
from src.services import search_transactions

file_path = OPEN_XLS


def test_search_transactions():
    assert search_transactions(file_path, "Аптеки") == (
        "[\n"
        "    {\n"
        '        "Дата операции": "17.01.2018 19:07:41",\n'
        '        "Дата платежа": "18.01.2018",\n'
        '        "Номер карты": "*7197",\n'
        '        "Статус": "OK",\n'
        '        "Сумма операции": -299.0,\n'
        '        "Валюта операции": "RUB",\n'
        '        "Сумма платежа": -299.0,\n'
        '        "Валюта платежа": "RUB",\n'
        '        "Кэшбэк": NaN,\n'
        '        "Категория": "Аптеки",\n'
        '        "MCC": 5912.0,\n'
        '        "Описание": "Дежурные аптеки",\n'
        '        "Бонусы (включая кэшбэк)": 5,\n'
        '        "Округление на инвесткопилку": 0,\n'
        '        "Сумма операции с округлением": 299.0\n'
        "    }\n"
        "]"
    )
