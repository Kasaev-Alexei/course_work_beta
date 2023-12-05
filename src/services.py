import pandas as pd
import json

from typing import Any
from src.log import log_utils

logging = log_utils()


def search_transactions(file_path: Any, query: str) -> Any:
    '''
    Принимает файл и запрос из описания, после ищет транзакции
    :param file_path: Путь до файла
    :param query: Запрос
    :return: json-ответ со всеми транзакциями
    '''
    df = pd.read_excel(file_path)
    filtered_df = df[df["Описание"].str.contains(query, case=False, na=False)]
    result = filtered_df.to_dict(orient="records")
    logging.info("Преобразование фильтрованного DataFrame в список словарей")
    return json.dumps(result, indent=4, ensure_ascii=False)
