import requests
import threading
from math import floor

apiKey = 'wYt_9D5jNJV7OTza9Dhp9Kx0vb3IHIUw'
secretKey = 'vwoLUogDZHxcaEsg-iuyh66EH33HjpD4'
loopInterval = 5

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
    print(dai)
    amountDai = float(dai['available'])

    if amountDai > 0.03:
        orderData = {'symbol':'USDTDAI', 'side': 'buy', 'quantity': floor(amountDai*100)/100-0.01, 'price': '0.999' }
        r = session.post('https://api.hitbtc.com/api/3/spot/order/', data = orderData)
        print('Buy USDT: ', r.json())

    # define balance USDT
    usdtBalance = session.get('https://api.hitbtc.com/api/3/spot/balance/USDT').json()
    print(usdtBalance)
    amountUsdt = float(usdtBalance['available'])

    if amountUsdt > 0.03:

        orderData = {'symbol':'USDTDAI', 'side': 'sell', 'quantity': floor(amountUsdt*100)/100-0.01, 'price': '1.005' }
        r = session.post('https://api.hitbtc.com/api/3/spot/order/', data = orderData)
        print('Sell USDT: ', r.json())

        
        
   
    
# using
setInterval(loop,loopInterval)
