from datetime import datetime, timedelta
import yfinance as yf
from sklearn.preprocessing import MinMaxScaler
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error
from .update_service import update



    
def predict_next_day(stock_symbol: str, model):
    
    # Preprocess the data
    X, y, scaler = preprocess_data(stock_symbol)

    # Make predictions
    y_pred = model.predict(X)
    y_pred = scaler.inverse_transform(y_pred)
    y_test_actual = scaler.inverse_transform(y.reshape(-1, 1))
    
    return {"predicted_price": y_pred[-1]}


def preprocess_data(stock_symbol):
    start_date = '2018-01-01'
    end_date = datetime.now()
    
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


def evaluate_models_performance_last_30_days(stock_symbol: str, model):
   # Preprocess the data
    X, y, scaler = preprocess_data(stock_symbol)

    # Make predictions
    y_pred = model.predict(X)
    y_pred = scaler.inverse_transform(y_pred)
    y_test_actual = scaler.inverse_transform(y.reshape(-1, 1))
    
    
    
    mae = mean_absolute_error(y_test_actual, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test_actual, y_pred))
    
    update(mae, rmse)
    
    return mae, rmse
    
    
    
        