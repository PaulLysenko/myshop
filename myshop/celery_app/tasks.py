import logging
from celery_app import celery_app


logger = logging.getLogger(__name__)


@celery_app.task
def test_task():
    """ """
    logger.critical('----------- >>>>>>>>>>>>> Hello world <<<<<<<<<<<<<<<<< ------------------')
