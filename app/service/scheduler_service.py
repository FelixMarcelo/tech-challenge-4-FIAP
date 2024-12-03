from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
from .update_service import model_metrics
from .prediction_service import evaluate_models_performance_last_30_days
from logging.handlers import RotatingFileHandler
import logging

logger = logging.getLogger(__name__)

scheduler = BackgroundScheduler()
    
def job_listener(event):
    if event.exception:
        logging.error(f"Metric update job failed: {event.job_id}")
    else:
        logging.info(f"Metric update job was executed successfully: {event.job_id}")

scheduler.add_job(evaluate_models_performance_last_30_days, 'interval', seconds=30)
scheduler.add_listener(job_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)

scheduler.start()

    