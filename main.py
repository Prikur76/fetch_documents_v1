import logging
import os
import shutil

import pandas as pd

import tools

logger = logging.getLogger(__name__)


def main():
    logging.basicConfig(
        format="[%(levelname)s] - %(asctime)s - %(name)s - %(message)s",
        level=logging.INFO
    )

    xlsx_file_path = 'Выгрузка файлов.xlsx'
    catalog_from = 'C:\\Users\\User\\YandexDisk-TPNEXT\\CATALOG'
    patterns = ['_ДК_', '_СТС_']
    limit_year = 2023

    try:
        target_contents = tools.fetch_target_content_from_xlsx(xlsx_file_path)
        contents = pd.DataFrame(tools.fetch_folders_content(
            catalog_from, patterns=patterns, limit=limit_year)
        )
        joined_content = target_contents.set_index('АМ.VIN')\
            .join(contents.set_index('vin'))

        for company, files in joined_content.values.tolist():
            if isinstance(files, list):
                company_path = os.path.join('.', company)
                tools.create_folder_for_file(company)
                for file in files:
                    current_file_path = file
                    new_file_path = os.path.join(
                        company_path, file.split('\\')[-1]
                    )
                    shutil.copy2(current_file_path, new_file_path)
    except Exception as err:
        logger.error(f'Error: {err}')


if __name__ == '__main__':
    main()
