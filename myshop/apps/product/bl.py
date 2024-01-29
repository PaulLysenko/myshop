from decimal import Decimal
import os
from datetime import datetime
import pandas
from django.conf import settings
from apps.product.constants import IMPORTED_FILE_PATH


def save_file_to_storage(imported_file):
    timestamp = datetime.now().strftime('%d_%m_%Y_%H_%M_%S')
    filename, file_extension = os.path.splitext(imported_file.name)
    new_filename = f"{timestamp}_{filename}{file_extension}"

    file_path = IMPORTED_FILE_PATH.format(settings.BASE_DIR, new_filename)

    with open(file_path, 'wb') as saved_file:
        saved_file.write(imported_file.read())

    return file_path


def parse_xlsx_file(file_path: str) -> list[dict[str, Decimal | str]]:

    pd_dataframe = pandas.read_excel(file_path)

    result = pd_dataframe.to_dict(orient='records')
    return result
