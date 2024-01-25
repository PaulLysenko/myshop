import csv

from celery_app import celery_app
from apps.product.bl import save_file_to_storage


@celery_app.task
def parsing_file(file_path):
    try:
        with open(file_path, "r") as f:
            reader = csv.reader(f)
            for row in reader:
                save_file_to_storage(row)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except csv.Error as e:
        print(f"CSV parsing error in file {file_path}: {e}")
