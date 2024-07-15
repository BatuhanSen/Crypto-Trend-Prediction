import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import LSTM, Dense

# Verileri yükleme
data = pd.read_csv('ETH-USD.csv')
closing_prices = data['Close'].values.reshape(-1, 1)
dates = data['Date'].values

# Verileri ölçeklendirme
scaler = MinMaxScaler(feature_range=(0, 1))
closing_prices_scaled = scaler.fit_transform(closing_prices)

# Eğitim ve test verilerini oluşturma
train_size = int(len(closing_prices_scaled) * 0.8)
train_data, test_data = closing_prices_scaled[:train_size], closing_prices_scaled[train_size:]
test_dates = dates[train_size + 10:]  # İlk 10 örnek zaman serisi uzunluğundan dolayı atlandı

def create_dataset(dataset, time_steps=1):
    dataX, dataY = [], []
    for i in range(len(dataset) - time_steps):
        a = dataset[i:(i + time_steps), 0]
        dataX.append(a)
        dataY.append(dataset[i + time_steps, 0])
    return np.array(dataX), np.array(dataY)

time_steps = 10  # Önceki 10 günü kullanarak tahmin yapalım
X_train, y_train = create_dataset(train_data, time_steps)
X_test, y_test = create_dataset(test_data, time_steps)

# LSTM modeli oluşturma
model = Sequential()
model.add(LSTM(units=50, return_sequences=True, input_shape=(X_train.shape[1], 1)))
model.add(LSTM(units=50))
model.add(Dense(1))
model.compile(optimizer='adam', loss='mean_squared_error')

# Modeli eğitme
model.fit(X_train, y_train, epochs=50, batch_size=32)

# Tahmin yapma
predicted_prices = model.predict(X_test)
predicted_prices = scaler.inverse_transform(predicted_prices.reshape(-1, 1))

# Gerçek fiyatları alın
actual_prices = scaler.inverse_transform(y_test.reshape(-1, 1))

# Tahminleri ve gerçek fiyatları tarihlerle birlikte karşılaştırma
for i in range(len(predicted_prices)):
    print(f"Tarih: {test_dates[i]} - Tahmin: {predicted_prices[i][0]:.2f} - Gerçek: {actual_prices[i][0]:.2f}")
