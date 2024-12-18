from fastapi import FastAPI, HTTPException
from prometheus_client import generate_latest
from starlette.responses import Response
from .service.prediction_service import evaluate_models_performance_last_30_days
from .service.prediction_service import predict_next_day, predict_input
import tensorflow as tf
from logging.handlers import RotatingFileHandler
import logging
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
from pydantic import ValidationError
from .dto.priceDTO import PriceListDTO


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.StreamHandler(),  # Send logs to stdout
        RotatingFileHandler("main.log", maxBytes=100000, backupCount=3)  # Optional file logging
    ]
)

logger = logging.getLogger(__name__)


app = FastAPI()

model = tf.keras.models.load_model('/app/app/lstm_stock_model.h5')
stock_symbol="AAPL"

@app.get("/")
async def read_root():
    return {"message": f"Welcome to the 4th tech challenge! Let's predict stock prices for {stock_symbol}. Go to /docs for testing"}


@app.get("/get-tomorrows-prediction")
async def predict():
    return predict_next_day(stock_symbol=stock_symbol, model=model)


@app.post("/input-data")
async def input_data(input_data: PriceListDTO):
    try:
        return predict_input(input=input_data, model=model)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
        


@app.post("/update_model_metrics") 
async def update_model_metrics():
    mse, rmse = evaluate_models_performance_last_30_days(stock_symbol=stock_symbol, model=model, n_days=30)
    return {"mse": f"Model mse updated to {mse}", "rmse": f"Model rmse updated to {rmse}"}  
      

@app.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type="text/plain")


scheduler = BackgroundScheduler()
    
def job_listener(event):
    if event.exception:
        logger.error(f"Metric update job failed: {event.job_id}")
    else:
        logger.info(f"Metric update job was executed successfully: {event.job_id}")

scheduler.add_job(update_model_metrics, 'interval', seconds=30)
scheduler.add_listener(job_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)

scheduler.start()
