from enum import IntEnum

IMPORTED_FILE_NAME = '{}-{}'
IMPORTED_FILE_DIRECTORY = 'xlsx_files'

DEFAULT_PRODUCT_CACHE_TIME = 300  # seconds
DEFAULT_PRODUCT_ALL_CACHE_KEY = 'product_all'


class FileImportStatus(IntEnum):
    NEW = 0
    SUCCESS = 10
    ERROR = 20

    @classmethod
    def choices(cls):
        return [(field.value, field.name) for field in cls]
