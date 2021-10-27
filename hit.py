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
    # print('Dai statement:', dai)
    amountDai = float(dai['available'])
    freeDai = floor(amountDai*998)/1000
    i = 0

    usdtPrice = session.get('https://api.hitbtc.com/api/3/public/orderbook/USDTDAI').json()
    bid = usdtPrice['bid']
    ask = usdtPrice['ask']

    while freeDai > 0.02:

       
        priceBuyI = float(bid[i][0])
        buyAmountI = float(bid[i][1])

        if priceBuyI > 0.9999:
            true

        elif buyAmountI < freeDai:
            orderData = {'symbol':'USDTDAI', 'side': 'buy', 'quantity': buyAmountI, 'price': priceBuyI +0.0001 }
            r = session.post('https://api.hitbtc.com/api/3/spot/order/', data = orderData)
            freeDai -= buyAmountI
            print('Buy USDT', r.json())
    
        else:
            orderData = {'symbol':'USDTDAI', 'side': 'buy', 'quantity': freeDai * (priceBuyI +0.0001), 'price': priceBuyI +0.0001 }
            r = session.post('https://api.hitbtc.com/api/3/spot/order/', data = orderData)
            print('Buy USDT', r.json())
            freeDai = 0
        print(i, '/n')
        i+=1
        

    # define balance USDT/////

    usdtBalance = session.get('https://api.hitbtc.com/api/3/spot/balance/USDT').json()
    # print('USDT statement:', usdtBalance)
    amountUSDT = float(usdtBalance['available'])
    freeUSDT = floor(amountUSDT*998)/1000
    i = 0

    while freeUSDT > 0.02:
               
        priceSellI = float(ask[i][0])
        sellAmountI = float(ask[i][1])

        if priceSellI < 1.0025:
            true

        elif sellAmountI < freeUSDT:
            orderData = {'symbol':'USDTDAI', 'side': 'sell', 'quantity': sellAmountI, 'price': priceSellI - 0.0001 }
            r = session.post('https://api.hitbtc.com/api/3/spot/order/', data = orderData)
            freeUSDT -= sellAmountI
            print('Sell USDT', r.json())
            print('Order data',orderData)
            print("freeUsdt", freeUSDT)
    
        else:
            orderData = {'symbol':'USDTDAI', 'side': 'sell', 'quantity': freeUSDT, 'price': priceSellI -0.0001 }
            r = session.post('https://api.hitbtc.com/api/3/spot/order/', data = orderData)
            freeUSDT = 0
            print('Sell USDT', r.json())
            print('Order data',orderData)
            print("freeUsdt", freeUSDT)

        print(i, '/n')
        i+=1


    # if amountUsdt > 0.03:

    #     #get order book
    #     usdtPrice = session.get('https://api.hitbtc.com/api/3/public/orderbook/USDTDAI').json()
    #     bid = usdtPrice['bid']
    #     ask = usdtPrice['ask']

    #     freeUSDT = floor(amountUsdt*100)/100-0.01
    #     print('free', freeUSDT, 'bid:', bid[0][0], 'ask:', ask[0][0] )

    #     if float(ask[0][0]) > 1.0031:
    #         print('1')
    #         if float(ask[0][1]) > freeUSDT:
    #             print(2)
    #             orderData = {'symbol':'USDTDAI', 'side': 'sell', 'quantity': freeUSDT, 'price': float(ask[0][0])-0.0001 }    
    #             r = session.post('https://api.hitbtc.com/api/3/spot/order/', data = orderData)
    #             print('Sell USDT: ', r.json())
    #         else:
    #             orderData = {'symbol':'USDTDAI', 'side': 'sell', 'quantity': float(ask[0][1]), 'price': float(ask[0][0])-0.0001 }    
    #             r = session.post('https://api.hitbtc.com/api/3/spot/order/', data = orderData)
    #             print('Sell USDT: ', r.json())

    #             freeUSDT -= float(ask[0][1])
    #             orderData = {'symbol':'USDTDAI', 'side': 'sell', 'quantity': freeUSDT, 'price': float(ask[1][0])-0.0001 }    
    #             r = session.post('https://api.hitbtc.com/api/3/spot/order/', data = orderData)
    #             print('Sell USDT: ', r.json())

        
        
   
    
# using
setInterval(loop,loopInterval)
