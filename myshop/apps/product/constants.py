from enum import IntEnum

IMPORTED_FILE_NAME = '{}-{}'
IMPORTED_FILE_DIRECTORY = 'xlsx_files'


class FileImportStatus(IntEnum):
    NEW = 0
    SUCCESS = 10
    ERROR = 20

    @classmethod
    def choices(cls):
        return [(field.value, field.name) for field in cls]
