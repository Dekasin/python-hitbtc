import requests
import threading
from math import floor

apiKey = 'wYt_9D5jNJV7OTza9Dhp9Kx0vb3IHIUw'
secretKey = 'vwoLUogDZHxcaEsg-iuyh66EH33HjpD4'
loopInterval = 5
priceBuy = 0.9992
priceSell = 1.0056

session = requests.session()
session.auth = (apiKey, secretKey)

def setInterval(func,time):
    e = threading.Event()
    while not e.wait(time):
        func()

def loop():
    # b = session.get('https://api.hitbtc.com/api/3/public/price/rate?from=ETH&to=BTC').json()
    
    # define balance DAI
    dai = session.get('https://api.hitbtc.com/api/3/spot/balance/DAI').json()
    print('Dai balance: ', dai)
    amountDai = float(dai['available'])
    freeDai = floor(amountDai*100)/100
    print("free DAi: ", freeDai)

    if amountDai > 0.02:
        orderData = {'symbol':'USDTDAI', 'side': 'buy', 'quantity': freeDai * priceBuy * 0.998, 'price': priceBuy }
        r = session.post('https://api.hitbtc.com/api/3/spot/order/', data = orderData)
        print('Buy USDT: ', r.json())

    # define balance USDT
    usdtBalance = session.get('https://api.hitbtc.com/api/3/spot/balance/USDT').json()
    print('USDT balance: ', usdtBalance)
    amountUsdt = float(usdtBalance['available'])
    freeUSDT = floor(amountUsdt*100)/100
    print("free USDT: ", freeUSDT)

    if amountUsdt > 0.02:
        orderData = {'symbol':'USDTDAI', 'side': 'sell', 'quantity': freeUSDT  * 0.998, 'price': priceSell } #0.998 comission 0.002
        print('sell data:', orderData)
        r = session.post('https://api.hitbtc.com/api/3/spot/order/', data = orderData)
        print('Sell USDT: ', r.json())

        
        
   
    
# using
setInterval(loop,loopInterval)
