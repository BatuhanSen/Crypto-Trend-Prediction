import numpy as np
import pandas as pd

def markov_chain_model(transition_matrix, initial_state, steps):
    current_state = initial_state

    for _ in range(steps):
        current_state = np.dot(current_state, transition_matrix)

    return current_state

if __name__ == "__main__":
    # Bitiş tarihini kullanıcıdan al
    end_date = input("Bitiş tarihini (YYYY-MM-DD formatında) girin: ")

    # Başlangıç tarihini belirle (verilen tarihten 20 gün önce)
    start_date = pd.to_datetime(end_date) - pd.Timedelta(days=20)

    # CSV dosyasından verileri oku
    data = pd.read_csv('ETC-USD.csv')
    data['Date'] = pd.to_datetime(data['Date'])

    # Verileri başlangıç ve bitiş tarihlerine göre filtrele
    filtered_data = data[(data['Date'] >= start_date) & (data['Date'] <= end_date)]
    end_date_filtered = filtered_data['Date'].iloc[-1]

    # En eski tarihi bul
    min_date = data['Date'].min()

    # Kullanılan veri aralığını yazdır
    print("Kullanılan veri aralığı:", start_date.strftime('%Y-%m-%d'), "-", end_date_filtered.strftime('%Y-%m-%d'))

    # "Adj. Close" fiyatlarını al
    adj_close_prices = filtered_data['Adj Close'].values

    # Günlük getirileri hesapla
    returns = np.log(adj_close_prices[1:] / adj_close_prices[:-1])

    # Getirileri kullanarak geçiş matrisini oluştur
    states = np.sign(returns)
    transition_matrix = np.zeros((3, 3))  # 3 states (decrease, unchanged, increase)
    for i in range(len(states) - 1):
        current_state = int(states[i] + 1)  # -1, 0, 1 to 0, 1, 2
        next_state = int(states[i + 1] + 1)
        transition_matrix[current_state][next_state] += 1

    # Herhangi bir satırda toplam sıfır olmaması için düzeltme yap
    transition_matrix += 1e-6
    transition_matrix = transition_matrix / transition_matrix.sum(axis=1, keepdims=True)

    # Başlangıç durumu
    initial_state = np.zeros(3)
    initial_state[1] = 1  # Başlangıç durumu: fiyat değişmez

    # Modeli kullanarak fiyat tahmini yap
    final_state = markov_chain_model(transition_matrix, initial_state, steps=7)

    # Tahminlerin yapılacağı son tarihi belirle
    prediction_date = pd.to_datetime(end_date_filtered) + pd.Timedelta(days=7)
    print("Bir hafta sonrası için tahminler (", prediction_date.strftime('%Y-%m-%d'), "):")
    print("Fiyat azalma olasılığı:", final_state[0])
    print("Fiyat değişmez olasılığı:", final_state[1])
    print("Fiyat artma olasılığı:", final_state[2])
