# from apscheduler.schedulers.background import BackgroundScheduler
# from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
# from .update_service import model_metrics
# from ..main import update_model_metrics
# from logging.handlers import RotatingFileHandler
# import logging

# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s [%(levelname)s] %(message)s',
#     handlers=[
#         logging.StreamHandler(),  # Send logs to stdout
#         RotatingFileHandler("scheduler.log", maxBytes=100000, backupCount=3)  # Optional file logging
#     ]
# )

# logger = logging.getLogger(__name__)

# scheduler = BackgroundScheduler()
    
# def job_listener(event):
#     if event.exception:
#         logger.error(f"Metric update job failed: {event.job_id}")
#     else:
#         logger.info(f"Metric update job was executed successfully: {event.job_id}")

# scheduler.add_job(update_model_metrics, 'interval', seconds=30)
# scheduler.add_listener(job_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)

# scheduler.start()

    