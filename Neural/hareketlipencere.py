import pandas as pd
import numpy as np

# Verileri yükleme
data = pd.read_csv('ETH-USD.csv')
prices = data['Close'].values

# Hareketli ortalama stratejisi
def moving_average_strategy(prices, window):
    moving_avg = np.convolve(prices, np.ones(window)/window, mode='valid')
    return moving_avg

window_size = 3  # Hareketli ortalama penceresi

# Sadece son %20 veriyi al
split_index = int(len(prices) * 0.8)
prices = prices[split_index:]

# Hareketli ortalama stratejisi ile gelecekteki fiyat yönünü tahmin etme
moving_avg_predictions = moving_average_strategy(prices, window_size)
predicted_directions = np.where(moving_avg_predictions[1:] > moving_avg_predictions[:-1], "Artacak", "Azalacak")

# Gerçek fiyat hareketleri
actual_directions = np.where(prices[1:] > prices[:-1], "Artacak", "Azalacak")

# Başarı oranını hesaplama
correct_predictions = 0
for i in range(len(predicted_directions)):
    if predicted_directions[i] == actual_directions[i]:
        correct_predictions += 1

total_predictions = len(predicted_directions)
success_rate = (correct_predictions / total_predictions) * 100

print("Başarı Oranı: {:.2f}%".format(success_rate))
