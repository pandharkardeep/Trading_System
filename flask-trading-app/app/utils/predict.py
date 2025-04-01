import tensorflow as tf
from utils.technical_indicators import fetch_stock_data, calculate_technical_indicators, preprocess_data
from tensorflow.keras.layers import LSTM, Dense, Dropout

def load_model():
    model = tf.keras.models.load_model('D:/Datahackproj/Trading-Project/flask-trading-app/Research/lstm_trading_model.h5')
    return model

def make_prediction(symbol):
    data = fetch_stock_data(symbol)
    if data.shape[0] == 0:
        return -1
    data = calculate_technical_indicators(data, symbol)
    data = preprocess_data(data)
    print(data.shape)
    model = tf.keras.Sequential([
        tf.keras.layers.Reshape((13, 1), input_shape=(13,)),  # Reshape for LSTM
        tf.keras.layers.LSTM(64, return_sequences=True),
        tf.keras.layers.LSTM(32),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dropout(0.3),
        tf.keras.layers.Dense(1, activation='sigmoid')
    ])
    model.load_weights('D:\\Datahackproj\\Trading-Project\\flask-trading-app\\Research\\lstm_trading_model.h5')
    print(data.shape)
    X = data.values
    prediction = model.predict(X)
    return prediction[0][0] > 0.5