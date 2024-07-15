import numpy as np
import pandas as pd
from hmmlearn import hmm

def prepare_data(end_date):
    # Başlangıç tarihini belirle (verilen tarihten 20 gün önce)
    start_date = pd.to_datetime(end_date) - pd.Timedelta(days=100)

    # CSV dosyasından verileri oku
    data = pd.read_csv('ETC-USD.csv')
    data['Date'] = pd.to_datetime(data['Date'])

    # Verileri başlangıç ve bitiş tarihlerine göre filtrele
    filtered_data = data[(data['Date'] >= start_date) & (data['Date'] <= end_date)]
    end_date_filtered = filtered_data['Date'].iloc[-1]

    # "Adj. Close" fiyatlarını al
    adj_close_prices = filtered_data['Adj Close'].values

    # Günlük getirileri hesapla
    returns = np.log(adj_close_prices[1:] / adj_close_prices[:-1])

    return returns

if __name__ == "__main__":
    # Bitiş tarihini kullanıcıdan al
    end_date = input("Bitiş tarihini (YYYY-MM-DD formatında) girin: ")

    # Veriyi hazırla
    returns = prepare_data(end_date)

    # HMM modelini oluştur
    model = hmm.GaussianHMM(n_components=3, covariance_type="full")

    # Veriyi modele uydur
    model.fit(returns.reshape(-1, 1))

    # Modeli kullanarak bir hafta sonrası için gizli durumları tahmin et
    predicted_hidden_states = model.predict(returns[-1].reshape(1, -1))

    # Son durumu al
    final_state = model.transmat_[predicted_hidden_states[0]]

    # Tahminlerin yapılacağı son tarihi belirle
    prediction_date = pd.to_datetime(end_date) + pd.Timedelta(days=7)
    print("Bir hafta sonrası için tahminler (", prediction_date.strftime('%Y-%m-%d'), "):")
    print("Fiyat azalma olasılığı:", final_state[0])
    print("Fiyat değişmez olasılığı:", final_state[1])
    print("Fiyat artma olasılığı:", final_state[2])
