from datetime import datetime, timedelta
import yfinance as yf
from sklearn.preprocessing import MinMaxScaler
import numpy as np
from sklearn.metrics import mean_squared_error
from .update_service import model_metrics



    
def predict_next_day(stock_symbol: str, model):
    
    # Preprocess the data
    X, y, scaler = preprocess_data(stock_symbol, n_days = 60)

    # Make predictions
    prediction = model.predict(X[-1].reshape(1, 60, 1))
    predicted_price = scaler.inverse_transform(prediction)[0][0]
    
    return {"predicted_price": predicted_price}


def preprocess_data(stock_symbol, n_days=60):
    today = datetime.now()
    n_days_ago = today - timedelta(days=n_days)
    data = yf.download(stock_symbol, start=n_days_ago.strftime("%Y-%m-%d"), end=today.strftime("%Y-%m-%d"))
            
    data = data[['Close']]
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(data)
    
    x, y = create_sequences(scaled_data, n_days)
    x = x.reshape(x.shape[0], x.shape[1], 1)
    
    return x, y, scaler


def create_sequences(data, seq_length):
    x, y = [], []
    for i in range(seq_length, len(data)):
        x.append(data[i-seq_length:i, 0])
        y.append(data[i, 0])
    return np.array(x), np.array(y)

def evaluate_models_performance_last_30_days(stock_symbol: str, model):
    # Preprocess the data
    X, y, scaler = preprocess_data(stock_symbol, n_days = 1800)
    predicted_prices = model.predict(X)

    # Inverse transform the predictions and actual values to get them back to original scale
    predicted_prices = scaler.inverse_transform(predicted_prices)
    y_test_actual = scaler.inverse_transform(y.reshape(-1, 1))
    
    mse = mean_squared_error(y_test_actual, predicted_prices)
    rmse = np.sqrt(mse)
    
    model_metrics_instancy = model_metrics()
    
    model_metrics_instancy.update(mse, rmse)
    
    return mse, rmse
    
    
    
        