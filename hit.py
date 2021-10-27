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
        print('Buy USDT', r.json())


    usdtBalance = session.get('https://api.hitbtc.com/api/3/spot/balance/USDT').json()
    print(usdtBalance)
    amountUsdt = float(usdtBalance['available'])

    if amountUsdt > 0.03:

        #get order book
        usdtPrice = session.get('https://api.hitbtc.com/api/3/public/orderbook/USDTDAI').json()
        bid = usdtPrice['bid']
        ask = usdtPrice['ask']

        freeUSDT = floor(amountUsdt*100)/100-0.01
        print('free', freeUSDT, 'bid:', bid[0][0], 'ask:', ask[0][0] )

        if float(ask[0][0]) > 1.0031:
            print('1')
            if float(ask[0][1]) > freeUSDT:
                print(2)
                orderData = {'symbol':'USDTDAI', 'side': 'sell', 'quantity': freeUSDT, 'price': float(ask[0][0])-0.0001 }    
                r = session.post('https://api.hitbtc.com/api/3/spot/order/', data = orderData)
                print('Sell USDT: ', r.json())
            else:
                orderData = {'symbol':'USDTDAI', 'side': 'sell', 'quantity': float(ask[0][1]), 'price': float(ask[0][0])-0.0001 }    
                r = session.post('https://api.hitbtc.com/api/3/spot/order/', data = orderData)
                print('Sell USDT: ', r.json())

                freeUSDT -= float(ask[0][1])
                orderData = {'symbol':'USDTDAI', 'side': 'sell', 'quantity': freeUSDT, 'price': float(ask[1][0])-0.0001 }    
                r = session.post('https://api.hitbtc.com/api/3/spot/order/', data = orderData)
                print('Sell USDT: ', r.json())

        
        
   
    
# using
setInterval(loop,loopInterval)
