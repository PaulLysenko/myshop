from datetime import datetime

from django.conf import settings

from apps.product.constants import IMPORTED_FILE_PATH


def save_file_to_storage(imported_file):

    file_path = IMPORTED_FILE_PATH.format(settings.BASE_DIR, datetime.now().strftime("%Y_%m_%d-%H_%M_%S"), imported_file.name)

    # save imported file to the hard drive
    with open(file_path, 'wb') as saved_file:
        saved_file.write(imported_file.read())

    return file_path
