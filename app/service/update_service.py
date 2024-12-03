import logging
from prometheus_client import Gauge


logger = logging.getLogger(__name__)

MEAN_SQRT_ERROR = Gauge('LSTM_mse', 'Mean Squared Error over the last 30 days')
ROOT_MEAN_SQRT_ERROR = Gauge('LSTM_rmse', 'Root Mean Squared Error over the last 30 days')

class model_metrics:        
    def update(mse, rmse):
        MEAN_SQRT_ERROR.set(mse)
        ROOT_MEAN_SQRT_ERROR.set(rmse)
        logger.info(f"The LSTM model mse was updated to {mse}.")
        logger.info(f"The LSTM model rmse was updated to {rmse}.")