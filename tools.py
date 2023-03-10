import os
from datetime import date

import pandas as pd


def create_folder_for_file(folder_name):
    """Возвращает папки для загрузки файлов"""
    return os.makedirs(folder_name, exist_ok=True)


def convert_date(file_date: str):
    """Конвертируем дату из файла в дату"""
    converted_date = date(
        int(file_date[:4]),
        int(file_date[4:6]),
        int(file_date[6:8])
    )
    if converted_date:
        return converted_date
    raise Exception('Ошибка даты')


def fetch_folders_content(catalog_from,
                          patterns=['_ДК_', '_СТС_'],
                          limit=2023):
    """Извлекает содержимое папок в каталоге"""
    folders_content = []
    for folder, subfolder, files in os.walk(catalog_from):
        vin = folder.split('\\')[-1]
        patterns_urls = [
            os.path.join(folder, file)
            for pattern in patterns
            for file in files if pattern in file
            if convert_date(file.split('_')[-1].split('.')[0]).year < limit
        ]

        folders_content.append(
            {
                'vin': vin,
                'files_urls': patterns_urls,
            }
        )
    return folders_content[1:]


def fetch_target_content_from_xlsx(xlsx_file_path):
    """Получаем список компаний и вин-номеров из файла"""
    xlsx_content = pd.read_excel(xlsx_file_path, engine='openpyxl')
    return xlsx_content
