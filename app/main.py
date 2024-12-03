
from fastapi import FastAPI
from prometheus_client import generate_latest
from starlette.responses import Response
from .service.prediction_service import evaluate_models_performance_last_30_days
from .service.prediction_service import predict_next_day
import tensorflow as tf

app = FastAPI()

model = tf.keras.models.load_model('stock_prediction_lstm_model.keras')
stock_symbol="AAPL"

@app.get("/")
def read_root():
    return {"message": f"Welcome to the 4th tech challenge! Let's predict stock prices for {stock_symbol}"}


@app.get("/get-prediction")
def predict():
    return predict_next_day(stock_symbol=stock_symbol, model=model)


@app.post("/update_model_metrics") 
async def update_model_metrics():
    mse, rmse = evaluate_models_performance_last_30_days(stock_symbol=stock_symbol, model=model)
    return {"mse": f"Model mse updated to {mse}", "rmse": f"Model rmse updated to {rmse}"}  
      

@app.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type="text/plain")
