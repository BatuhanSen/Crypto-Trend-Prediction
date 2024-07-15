import numpy as np
import pandas as pd

def monte_carlo_simulation(closing_prices, num_simulations, num_days):
    returns = np.log(closing_prices / closing_prices.shift(1))
    mean_daily_return = returns.mean()
    std_daily_return = returns.std()

    simulations = np.zeros((num_days, num_simulations))
    simulations[0] = closing_prices.iloc[-1]

    for i in range(1, num_days):
        noise = np.random.normal(mean_daily_return, std_daily_return, num_simulations)
        simulations[i] = simulations[i - 1] * (1 + noise)

    return simulations

if __name__ == "__main__":
    # Bitiş tarihini kullanıcıdan al
    end_date = input("Bitiş tarihini (YYYY-MM-DD formatında) girin: ")

    # CSV dosyasından verileri oku
    data = pd.read_csv('ETC-USD.csv')
    data['Date'] = pd.to_datetime(data['Date'])

    # En eski tarihi bul
    min_date = data['Date'].min()

    # Başlangıç tarihini belirle (en eski tarih)
    start_date = min_date

    # Verileri başlangıç ve bitiş tarihlerine göre filtrele
    filtered_data = data[(data['Date'] >= start_date) & (data['Date'] <= end_date)]
    end_date_filtered = filtered_data['Date'].iloc[-1]

    # Kullanılan veri aralığını yazdır
    print("Kullanılan veri aralığı:", start_date.strftime('%Y-%m-%d'), "-", end_date_filtered.strftime('%Y-%m-%d'))

    # "Close" fiyatlarını al
    closing_prices = filtered_data['Close']

    # Monte Carlo simülasyonu için parametreler
    num_simulations = 1000
    num_days = 7

    # Monte Carlo simülasyonunu çalıştır
    simulations = monte_carlo_simulation(closing_prices, num_simulations, num_days)

    # Tahminlerin yapılacağı son tarihi belirle
    prediction_date = pd.to_datetime(end_date_filtered) + pd.Timedelta(days=7)
    print("Bir hafta sonrası için tahminler (", prediction_date.strftime('%Y-%m-%d'), "):")

    # Tahminlerin yapılacağı son günün fiyatları
    final_prices = simulations[-1]

    # Fiyat değişim tahminleri
    increase_probability = np.mean(final_prices > closing_prices.iloc[-1])
    decrease_probability = np.mean(final_prices < closing_prices.iloc[-1])
    unchanged_probability = 1 - increase_probability - decrease_probability

    print("Fiyat azalma olasılığı:", decrease_probability)
    print("Fiyat değişmez olasılığı:", unchanged_probability)
    print("Fiyat artma olasılığı:", increase_probability)
