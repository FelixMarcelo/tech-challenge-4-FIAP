import logging
from logging.handlers import RotatingFileHandler
from prometheus_client import Gauge


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.StreamHandler(),  # Send logs to stdout
        RotatingFileHandler("update.log", maxBytes=100000, backupCount=3)  # Optional file logging
    ]
)

logger = logging.getLogger(__name__)

MEAN_SQRT_ERROR = Gauge('LSTM_mse', 'Mean Squared Error over the last 30 days')
ROOT_MEAN_SQRT_ERROR = Gauge('LSTM_rmse', 'Root Mean Squared Error over the last 30 days')

def update(msa, rmse):
    MEAN_SQRT_ERROR.set(msa)
    ROOT_MEAN_SQRT_ERROR.set(rmse)
    logger.info(f"The LSTM model mse was updated to {msa}.")
    logger.info(f"The LSTM model rmse was updated to {rmse}.")     
    