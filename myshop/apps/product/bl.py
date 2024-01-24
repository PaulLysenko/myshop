from decimal import Decimal
import pandas
from django.conf import settings
from apps.product.constants import IMPORTED_FILE_PATH
from apps.product.models import FileImport


def save_file_to_storage(imported_file):

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
