from project.celery import app
from django.core.management import call_command
import logging

logger = logging.getLogger(__name__)

@app.task
def update_search_vectors():
    logger.info("Starting search vector update task")
    try:
        call_command('update_search_vectors')
        logger.info("Search vector update completed successfully")
    except Exception as e:
        logger.error(f"Error updating search vectors: {str(e)}")
    return "Search vector update task completed"