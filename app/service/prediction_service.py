from datetime import datetime, timedelta
import yfinance as yf
from sklearn.preprocessing import MinMaxScaler
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error
from .update_service import update
from fastapi import HTTPException
from ..dto.priceDTO import PriceListDTO
import pandas as pd

    
def predict_next_day(stock_symbol: str, model):
    
    # Preprocess the data
    X, y, scaler = preprocess_data(stock_symbol)

    # Make predictions
    y_pred = model.predict(X)
    y_pred = scaler.inverse_transform(y_pred)
    y_test_actual = scaler.inverse_transform(y.reshape(-1, 1))
    
    return {"predicted_price": round(float(y_pred[-1]), 2)}


def preprocess_data(stock_symbol):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    
    data = yf.download(stock_symbol, start=start_date, end=end_date)
            
    data = data[['Adj Close']].rename(columns={'Adj Close': 'Close'})
    scaler = MinMaxScaler(feature_range=(0, 1))
    data['Close'] = scaler.fit_transform(data[['Close']])
    data_values = data.values
    
    x, y = create_sequences(data_values)
    x = x.reshape((x.shape[0], x.shape[1], 1))
    
    return x, y, scaler


def create_sequences(data, seq_length=60):
    X, y = [], []
    for i in range(seq_length, len(data)):
        X.append(data[i-seq_length:i, 0]) # 60 dias anteriores
        y.append(data[i, 0]) # Próximo valor
    return np.array(X), np.array(y)


def evaluate_models_performance_last_30_days(stock_symbol: str, model, n_days: int):
    if n_days > 365:
        raise HTTPException(status_code=400, detail="n_days needs to be less than or equal to 365")
   # Preprocess the data
    X, y, scaler = preprocess_data(stock_symbol)

    # Make predictions
    y_pred = model.predict(X)
    y_pred = scaler.inverse_transform(y_pred)
    y_test_actual = scaler.inverse_transform(y.reshape(-1, 1))
    
    mae = mean_absolute_error(y_test_actual[-n_days:], y_pred[-n_days:])
    rmse = np.sqrt(mean_squared_error(y_test_actual[-n_days:], y_pred[-n_days:]))
    
    update(mae, rmse)
    
    return mae, rmse

def predict_input(input: PriceListDTO, model):
    new_data_df = pd.DataFrame(input.priceList, columns=['Close'])

    scaler = MinMaxScaler(feature_range=(0, 1))
    new_data_scaled = scaler.fit_transform(new_data_df[['Close']])

    sequence = new_data_scaled[-60:].reshape((1, 60, 1))  

    predicted_price = model.predict(sequence)

    predicted_price_unscaled = scaler.inverse_transform(predicted_price)

    return {"predicted_price": round(float(predicted_price_unscaled), 2)}
    
    
    
        