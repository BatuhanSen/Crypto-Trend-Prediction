import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from keras_tuner.tuners import RandomSearch
from keras_tuner.engine.hyperparameters import HyperParameters

# CSV dosyasını yükle
data = pd.read_csv('ETH-USD.csv')
dates = pd.to_datetime(data['Date'])  # Tarihleri al

# 'Adj Close' değerlerini al
ethereum_prices = data['Adj Close'].values

# Veriyi ölçeklendir
scaler = MinMaxScaler()
ethereum_prices_scaled = scaler.fit_transform(ethereum_prices.reshape(-1, 1))

# Özellikler ve hedef değişkeni ayarla
X = np.arange(len(ethereum_prices)).reshape(-1, 1)
y = ethereum_prices_scaled.flatten()

# Veriyi eğitim ve test kümelerine bölelim
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

# Hyperparameter tuning için Keras Tuner'ı ayarla
def build_model(hp):
    model = tf.keras.Sequential()
    model.add(tf.keras.layers.Dense(units=hp.Int('units', min_value=32, max_value=256, step=32), activation='relu', input_shape=(1,)))
    for i in range(hp.Int('num_layers', 1, 3)):
        model.add(tf.keras.layers.Dense(units=hp.Int(f'layer_{i}_units', min_value=32, max_value=256, step=32), activation='relu'))
        model.add(tf.keras.layers.Dropout(0.2))
    model.add(tf.keras.layers.Dense(1, activation='linear'))
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model

tuner = RandomSearch(
    build_model,
    objective='val_loss',
    max_trials=25,
    directory='my_dir',
    project_name='ethereum_price_prediction2'
)

# Modeli eğitim verisiyle uygun hiperparametrelerle oluştur
tuner.search(X_train, y_train, epochs=100, batch_size=32, validation_split=0.2)

# En iyi modeli seç
best_model = tuner.get_best_models(num_models=1)[0]

# Test verileri üzerinde tahmin yap
y_pred_scaled = best_model.predict(X_test)
y_pred_inverse = scaler.inverse_transform(y_pred_scaled)

# Gerçek değerleri ters ölçekleme yaparak elde et
y_test_inverse = scaler.inverse_transform(y_test.reshape(-1, 1))
y_test_inverse = y_test_inverse.flatten()

# Tahminleri ve gerçek değerleri tarihlerle birlikte karşılaştır (test verileri için)
for i in range(len(y_pred_inverse)):
    print(f"Tarih: {dates[X_test[i][0]]}, Gerçek Değer: {y_test_inverse[i]:.2f}, Tahmin: {y_pred_inverse[i][0]:.2f}")
