from decimal import Decimal
import pandas
from django.conf import settings
from apps.product.constants import IMPORTED_FILE_PATH


def save_file_to_storage(imported_file):
    # todo HW: add import time to path
    # like 18_12_2024_20_10_35_myshop1.xlsx

    file_path = IMPORTED_FILE_PATH.format(settings.BASE_DIR, imported_file.name)

    # save imported file to the hard drive
    with open(file_path, 'wb') as saved_file:
        saved_file.write(imported_file.read())

    return file_path


def parse_xlsx_file(file_path: str) -> list[dict[str, Decimal | str]]:

    pd_dataframe = pandas.read_excel(file_path)
    # check headers
    # normalize data

    result = pd_dataframe.to_dict(orient='records')
    return result
