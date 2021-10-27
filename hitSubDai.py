import requests
import threading
from math import floor
import time

# seconds passed since epoch


apiKey = 'MOa7_xGmOzehNkVrOFZDhd2gw4sD3X2M'
secretKey = 'R8eM0vmcpx5OtQl08gdhEoSFzAmUlDYh'
loopInterval = 5
priceBuy = 0.9992
priceSell = 1.0056


session = requests.session()
session.auth = (apiKey, secretKey)

def setInterval(func,time):
    e = threading.Event()
    while not e.wait(time):
        func()

def getBalance():
    dai = session.get('https://api.hitbtc.com/api/3/spot/balance/DAI').json()
    print('Dai reserved:', dai['reserved'])
    usdtBalance = session.get('https://api.hitbtc.com/api/3/spot/balance/USDT').json()
    print('USDT reserved:', usdtBalance['reserved'])

def showTime():
    seconds = time.time()
    local_time = time.ctime(seconds)
    print("Local time:", local_time)
    


def loop():
    # sample GET
    # b = session.get('https://api.hitbtc.com/api/3/public/price/rate?from=ETH&to=BTC').json()
    count = 0

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
            True

        elif buyAmountI < freeDai:
            orderData = {'symbol':'USDTDAI', 'side': 'buy', 'quantity': buyAmountI, 'price': priceBuyI +0.00001 }
            r = session.post('https://api.hitbtc.com/api/3/spot/order/', data = orderData)
            freeDai -= buyAmountI
            count += 1
            print('Order №', count )
            print('Buy USDT', r.json())

    
        else:
            orderData = {'symbol':'USDTDAI', 'side': 'buy', 'quantity': freeDai * (priceBuyI +0.00001), 'price': priceBuyI +0.00001 }
            r = session.post('https://api.hitbtc.com/api/3/spot/order/', data = orderData)
            count += 1
            print('Order №', count )
            print('Buy USDT', r.json())
            freeDai = 0

        # print(i, '/n')
        
        i+=1
        getBalance()
        showTime()

    # define balance USDT/////

    usdtBalance = session.get('https://api.hitbtc.com/api/3/spot/balance/USDT').json()
    # print('USDT statement:', usdtBalance)
    amountUSDT = float(usdtBalance['available'])
    freeUSDT = floor(amountUSDT*998)/1000
    i = 0

    while freeUSDT > 0.02:
               
        priceSellI = float(ask[i][0])
        sellAmountI = float(ask[i][1])

        if priceSellI < 1.003:
            True

        elif sellAmountI < freeUSDT:
            orderData = {'symbol':'USDTDAI', 'side': 'sell', 'quantity': sellAmountI, 'price': priceSellI - 0.00001 }
            r = session.post('https://api.hitbtc.com/api/3/spot/order/', data = orderData)
            count += 1
            print('Order №', count )
            freeUSDT -= sellAmountI
            print('Sell USDT', r.json())
            print('Order data',orderData)
            print("freeUsdt", freeUSDT)
    
        else:
            orderData = {'symbol':'USDTDAI', 'side': 'sell', 'quantity': freeUSDT, 'price': priceSellI -0.00001 }
            r = session.post('https://api.hitbtc.com/api/3/spot/order/', data = orderData)
            count += 1
            print('Order №', count )
            freeUSDT = 0
            print('Sell USDT', r.json())
            print('Order data',orderData)
            print("freeUsdt", freeUSDT)

        # print(i, '/n')

        i+=1
        getBalance()
        showTime()

# define balance BTC/////

    btcBalance = session.get('https://api.hitbtc.com/api/3/spot/balance/BTC').json()
    # print('BTC statement:', btcBalance)
    amountBtc = float(btcBalance['available'])
    freeBtc = floor(amountBtc * 998000)/1000000
    i = 0

    btcPrice = session.get('https://api.hitbtc.com/api/3/public/orderbook/PROBTC').json()
    
    bid = btcPrice['bid']
    ask = btcPrice['ask']
    print(freeBtc)

    while freeBtc > 0.000005:

       
        priceBuyI = float(bid[i][0])
        buyAmountI = float(bid[i][1])
        print('btcPrice:', priceBuyI, buyAmountI)
        if priceBuyI > 0.000031:
            True

        elif buyAmountI < freeBtc:
            orderData = {'symbol':'PROBTC', 'side': 'buy', 'quantity': buyAmountI, 'price': priceBuyI +0.000000001 }
            r = session.post('https://api.hitbtc.com/api/3/spot/order/', data = orderData)
            freeBTC -= buyAmountI
            
            print('Buy PRO', r.json())

    
        else:
            orderData = {'symbol':'PROBTC', 'side': 'buy', 'quantity': freeBtc / (priceBuyI + 0.000000001), 'price': priceBuyI + 0.000000001 }
            r = session.post('https://api.hitbtc.com/api/3/spot/order/', data = orderData)
            
            print('Buy PRO', r.json())
            freeBtc = 0

        # print(i, '/n')
        
        i += 1
        getBalance()
        showTime()

# define balance PRO/////

    proBalance = session.get('https://api.hitbtc.com/api/3/spot/balance/PRO').json()
    print('PRO statement:', proBalance)
    proAmount = float(proBalance['available'])
    freePro = floor(proAmount * 998)/1000
    i = 0

    while freePro > 0.2:
               
        priceSellI = float(ask[i][0])
        sellAmountI = float(ask[i][1])

        if priceSellI < 0.000033:
            True

        elif sellAmountI < freePro:
            orderData = {'symbol':'PROBTC', 'side': 'sell', 'quantity': sellAmountI, 'price': priceSellI - 0.000000001 }
            r = session.post('https://api.hitbtc.com/api/3/spot/order/', data = orderData)
           
            freePro -= sellAmountI
            print('Sell PRO', r.json())
            print('Order data',orderData)
            print("freePRO", freePro)
    
        else:
            orderData = {'symbol':'PROBTC', 'side': 'sell', 'quantity': freePro, 'price': priceSellI -0.000000001 }
            r = session.post('https://api.hitbtc.com/api/3/spot/order/', data = orderData)
            
            freePro = 0
            print('Sell PRO', r.json())
            print('Order data',orderData)
            print("freePRO", freePro)

        # print(i, '/n')

        i+=1
        getBalance()
        showTime()    
        
   
    
# using
setInterval(loop,loopInterval)
