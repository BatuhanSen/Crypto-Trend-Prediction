# Sonuçları içeren dosyayı açma
with open('sonuc.txt', 'r') as file:
    lines = file.readlines()

# Tarih, tahmin ve gerçek fiyatları saklamak için listeler
dates = []
predicted_prices = []
actual_prices = []

# Satırları döngü ile işleme alma
for line in lines:
    parts = line.strip().split(' - ')
    date = parts[0].split(': ')[1]
    predicted_price = float(parts[1].split(': ')[1])
    actual_price = float(parts[2].split(': ')[1])
    
    dates.append(date)
    predicted_prices.append(predicted_price)
    actual_prices.append(actual_price)

# Ticaret stratejisi simülasyonu
initial_balance = 10000
balance = initial_balance
stocks = 0
transactions = []

for i in range(len(predicted_prices)):
    if i == 0:
        continue
    if predicted_prices[i] > predicted_prices[i - 1]:
        max_stocks_to_buy = int(balance / actual_prices[i])  # Yeterli parayla alınabilecek maksimum hisse miktarı
        stocks_to_buy = balance / actual_prices[i]  # İstediğiniz miktarda hisse alımı
        stocks_to_buy = min(stocks_to_buy, max_stocks_to_buy)  # İstediğiniz miktarı ve maksimum alınabilecek miktarı karşılaştırma
        if stocks_to_buy > 0:  # Hisse alınacak miktar pozitif ise alım yapın
            cost = stocks_to_buy * actual_prices[i]
            stocks += stocks_to_buy
            balance -= cost
            transactions.append(f"Alım - Tarih: {dates[i]}, Hisse Miktarı: {stocks_to_buy:.2f}, Fiyat: {actual_prices[i]:.2f}")
    elif stocks > 0:  # Sadece elinizde hisse varken satış yapın
        stocks_to_sell = stocks  # İstediğiniz miktarda hisse satışı
        income = stocks_to_sell * actual_prices[i]
        balance += income
        stocks -= stocks_to_sell
        transactions.append(f"Satış - Tarih: {dates[i]}, Hisse Miktarı: {stocks_to_sell:.2f}, Fiyat: {actual_prices[i]:.2f}")

# Sonuçları görüntüleme
print("İlk Bakiye: {:.2f}".format(initial_balance))
print("Son Bakiye: {:.2f}".format(balance))
print("Toplam Kazanç / Kayıp: {:.2f}".format(balance - initial_balance))
print("Yapılan İşlemler:")
for transaction in transactions:
    print(transaction)
