import json
import math
from datetime import datetime
from settings import OPEN_XLS, OPEN_JSON
import pandas as pd

from src.log import log_utils
from src.views import get_stocks, get_currencies
from typing import Any

logging = log_utils()


def get_greeting():
    """
    Вывод времени
    :return: string
    """
    current_time = datetime.now().hour
    log_utils().info("Дата запускается get_getting")
    if 0 <= current_time < 4:
        return "Доброй ночи!"
    elif 4 > current_time <= 12:
        return "Доброе утро!"
    elif 12 > current_time <= 17:
        return "Добрый день!"
    else:
        return "Добрый вечер!"


def transactions_xlsx_open() -> Any:
    """
    Функция считывает файлы excel
    :param: path
    :return: dict
    """
    try:
        return pd.read_excel(OPEN_XLS)
    except ValueError:
        logging.error("Ошибка чтения operations.xls")
        return "Ошибка чтения файла excel"


def process_data(start: str) -> list[dict]:
    start_date = pd.to_datetime(start)
    df = transactions_xlsx_open()
    data = []
    df = df.dropna(subset=['Номер карты'])
    df['Дата операции'] = pd.to_datetime(df['Дата операции'], format='%d.%m.%Y %H:%M:%S')
    df = df[df['Дата операции'] >= start_date]
    for card_num in df['Номер карты'].unique():
        total_spent = 0
        cashback = 0
        card_data = df[df['Номер карты'] == card_num]
        for index, row in card_data.iterrows():
            total_spent += row['Сумма платежа']
            if total_spent < 0:
                cashback += math.fabs(row['Сумма платежа'] // 100)
            cashback += row.get("Кэшбэк") if not math.isnan(row.get("Кэшбэк")) else 0
        data.append({
            "last_digits": card_num[-4:],
            "total_spent": total_spent,
            "cashback": cashback
        })
    logging.info("Функция process_data() отработала")
    return data


def top_transactions(transactions: pd.DataFrame) -> list[dict]:
    transactions = transactions.sort_values(by='Дата операции').nlargest(5, 'Сумма платежа')
    top = []
    for index, row in transactions.iterrows():
        top.append({
            "date": row['Дата операции'],
            "amount": float(row['Сумма платежа']),
            "category": row['Категория'],
            "description": row['Описание']
        })
    logging.info("Функция top_transactions() отработала")
    return top


def open_json(path, key):
    """
    Открывает json файл
    :param path: путь к файлу
    :param key: ключ словаря в json
    :return: список валют
    """
    with open(path, 'r') as fcc_file:
        logging.info("Файл json прочитан")
        return json.load(fcc_file)[key]


def collect_response() -> dict:
    return {
        "greeting": get_greeting(),
        "cards": process_data("2018-05-21 00:00:00"),
        "top_transactions": top_transactions(transactions_xlsx_open()),
        "currency_rates": get_currencies(open_json(OPEN_JSON, 'user_currencies')),
        "stock_prices": get_stocks(open_json(OPEN_JSON, 'user_stocks'))
    }
