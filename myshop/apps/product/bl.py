from decimal import Decimal
import pandas
from django.conf import settings


def save_file_to_storage(file):
    # todo HW: add import time to path
    # like 18_12_2024_20_10_35_myshop1.xlsx
    file_path = str(settings.BASE_DIR) + '/xlsx_files/' + file.name

    with open(file_path, 'wb') as saved_file:
        for chunk in file.chunks():
            saved_file.write(chunk)

    return file_path


def parse_xlsx_file(file_path: str) -> list[dict[str, Decimal | str]]:

    pd_dataframe = pandas.read_excel(file_path)
    # check headers
    # normalize data
    # validate data
    result = pd_dataframe.to_dict(orient='records')
    return result
