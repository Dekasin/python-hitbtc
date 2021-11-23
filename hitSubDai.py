import requests
import threading
from math import floor
import time
from KEYS_DAI import *



# seconds passed since epoch
local_time = time.ctime()
print("SCRIPT START AT:", local_time)


LOOP_INTERVAL = 5

USDT_PRICE_BUY_MAX = 0.9999
USDT_PRICE_SELL_MIN = 1.0045

PRO_PRICE_BUY_MAX = 0.000030
proPriceBuy01 = 0.0000326
proPriceSellMin = 0.000047
proPriceSell01 = 0.000042

FACTOR_MIN = 0.15


session = requests.session()
session.auth = (API_KEY, SECRET_KEY)

        # DELETE /api/3/spot/order

clearOrder = session.delete('https://api.hitbtc.com/api/3/spot/order').json()
print('DELETE orders \n: ', clearOrder)
print('_ _ _ _ _ _ _ _ _ _ _ _ _ ')
print('_ _ _ _ _ _ _ _ _ _ _ _ _ ')

def setInterval(func,time):
    try:
        e = threading.Event()
        while not e.wait(time):
            func()
    except:
        print("disconnect")
        session = requests.session()
        session.auth = (API_KEY, SECRET_KEY)

def getBalance():
    dai = session.get('https://api.hitbtc.com/api/3/spot/balance/DAI').json()
    print('Dai reserved:', dai['reserved'])
    usdtBalance = session.get('https://api.hitbtc.com/api/3/spot/balance/USDT').json()
    print('USDT reserved:', usdtBalance['reserved'])
    btcBalance = session.get('https://api.hitbtc.com/api/3/spot/balance/BTC').json()
    print('BTC reserved:', btcBalance['reserved'])
    proBalance = session.get('https://api.hitbtc.com/api/3/spot/balance/PRO').json()
    print('PRO reserved:', proBalance['reserved'])
    

def showTime():
    # seconds = time.time()
    local_time = time.ctime()
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
    

    usdtPrice = session.get('https://api.hitbtc.com/api/3/public/orderbook/USDTDAI').json()
    bid = usdtPrice['bid']
    ask = usdtPrice['ask']
    i = 0
    while freeDai > 0.02:

       
        priceBuyI = float(bid[i][0])
        buyAmountI = float(bid[i][1])

        if priceBuyI > USDT_PRICE_BUY_MAX:
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

        print(i, '\n')
        
        i += 1
        

    # define balance USDT/////

    usdtBalance = session.get('https://api.hitbtc.com/api/3/spot/balance/USDT').json()
    # print('USDT statement:', usdtBalance)
    amountUSDT = float(usdtBalance['available'])
    freeUSDT = floor(amountUSDT*998)/1000
    i = 0

    while freeUSDT > 0.02:
               
        priceSellI = float(ask[i][0])
        sellAmountI = float(ask[i][1])

        if priceSellI < USDT_PRICE_SELL_MIN:
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

            print('_______')
            showTime()
            getBalance()
    
        else:
            orderData = {'symbol':'USDTDAI', 'side': 'sell', 'quantity': freeUSDT, 'price': priceSellI -0.00001 }
            r = session.post('https://api.hitbtc.com/api/3/spot/order/', data = orderData)
            count += 1
            print('Order №', count )
            freeUSDT = 0
            print('Sell USDT', r.json())
            print('Order data',orderData)
            print("freeUsdt", freeUSDT)

            print('_______')
            showTime()
            getBalance()

        i +=1 
        print(i, '\n')

        
        

# define balance BTC/////

    btcBalance = session.get('https://api.hitbtc.com/api/3/spot/balance/BTC').json()
    # print('BTC statement:', btcBalance)
    amountBtc = float(btcBalance['available'])
    freeBtc = floor(amountBtc * 998000)/1000000
    

    btcPrice = session.get('https://api.hitbtc.com/api/3/public/orderbook/PROBTC').json()
    
    bid = btcPrice['bid']
   
    ask = btcPrice['ask']

    # print('bid  =  ', bid)
    # print('ask = ' , ask)
    # print(freeBtc)
    
    i = 0
    k = 0
    while freeBtc > 0.000005:
        
        

        priceBuyI = float(bid[i][0])
        buyAmountI = float(bid[i][1])
        print('ByyAmount:', buyAmountI,  "free BTC:", freeBtc,'\n Price =', priceBuyI, 'i=', i )

        # print('btcPrice:', priceBuyI, buyAmountI,  )
        if priceBuyI > float(ask[0][0]) * 0.98:
            True

        elif priceBuyI > proPriceBuy01:
            True

        elif (priceBuyI > PRO_PRICE_BUY_MAX) and freeBtc * FACTOR_MIN > 0.000005 and k <= 2:
            
            if buyAmountI > (freeBtc * FACTOR_MIN) / priceBuyI:
                buyAmountI = (freeBtc * FACTOR_MIN) / priceBuyI + 0.00000001
            orderData = {'symbol':'PROBTC', 'side': 'buy', 'quantity': buyAmountI, 'price': priceBuyI +0.00000001 }
            r = session.post('https://api.hitbtc.com/api/3/spot/order/', data = orderData)
            freeBtc = freeBtc - buyAmountI * (priceBuyI + 0.00000001)
            k +=1
            
            print('Buy PRO  __MIN__0.1__', r.json())
            print('FREE BTC_______', freeBtc)
            print('_______')
            showTime()
            getBalance()

        elif (priceBuyI > PRO_PRICE_BUY_MAX)  and i > 2:
            False


        elif buyAmountI < freeBtc / priceBuyI:
            orderData = {'symbol':'PROBTC', 'side': 'buy', 'quantity': buyAmountI, 'price': priceBuyI +0.00000001 }
            r = session.post('https://api.hitbtc.com/api/3/spot/order/', data = orderData)
            freeBtc = freeBtc - buyAmountI * (priceBuyI + 0.00000001)
            k +=1

            print('Buy PRO  min', r.json())
            print('_______')
            showTime()
            getBalance()
    
        else:
            orderData = {'symbol':'PROBTC', 'side': 'buy', 'quantity': freeBtc / (priceBuyI + 0.00000001), 'price': priceBuyI + 0.00000001 }
            r = session.post('https://api.hitbtc.com/api/3/spot/order/', data = orderData)
            k +=1
            print('Buy PRO allBTC', r.json())
            freeBtc = 0

            print('_______')
            showTime()
            getBalance()
        i += 1  

        print(i, '\n')
        
    print('______')    
    
    print('END While BTC')
    print('______')       
        

# define balance PRO/////

    proBalance = session.get('https://api.hitbtc.com/api/3/spot/balance/PRO').json()
    # print('PRO statement:', proBalance)
    proAmount = float(proBalance['available'])
    freePro = floor(proAmount * 998)/1000
    
    i = 0
    orderCounter = 0
    while freePro >= 0.1:
               
        priceSellI = float(ask[i][0])
        sellAmountI = float(ask[i][1])
        print(priceSellI, sellAmountI)
        
        if priceSellI < float(bid[0][0]) * 1.02:
            False
        elif priceSellI < proPriceSell01:
            False
        elif (priceSellI < proPriceSellMin) and freePro * FACTOR_MIN >= 0.1 and orderCounter <= 2:
            # True
            if sellAmountI > freePro * FACTOR_MIN:
                sellAmountI = freePro * FACTOR_MIN

            orderData = {'symbol':'PROBTC', 'side': 'sell', 'quantity': sellAmountI, 'price': priceSellI -0.000000001 }
            r = session.post('https://api.hitbtc.com/api/3/spot/order/', data = orderData)
            orderCounter += 1
            freePro -= (sellAmountI)
            print('Sell PRO __MIN___0.1__', r.json())
            print('Order data',orderData)
            print("freePRO", freePro)
            print('_______')
            showTime()
            getBalance()

        elif (priceSellI < proPriceSellMin) and orderCounter > 2:
            True    

        elif sellAmountI < freePro:
            orderData = {'symbol':'PROBTC', 'side': 'sell', 'quantity': sellAmountI, 'price': priceSellI - 0.000000001 }
            r = session.post('https://api.hitbtc.com/api/3/spot/order/', data = orderData)
            orderCounter += 1
            freePro -= sellAmountI
            print('Sell PRO', r.json())
            print('Order data',orderData)
            print("freePRO", freePro)
            print('_______')
            showTime()
            getBalance()
    
        else:
            orderData = {'symbol':'PROBTC', 'side': 'sell', 'quantity': floor(freePro * 10)/10, 'price': priceSellI -0.000000001 }
            r = session.post('https://api.hitbtc.com/api/3/spot/order/', data = orderData)
            orderCounter += 1
            freePro = 0
            print('Sell PRO all', r.json())
            print('Order data',orderData)
            print("freePRO", freePro)
            print('_______')
            showTime()
            getBalance()
        i += 1
        print(i, '\n')

    print('______')    
    
    print('END While PRO')
    print('______')   
    
# using
setInterval(loop,LOOP_INTERVAL)


    # DELETE /api/3/spot/order

# clearOrder = session.delete('https://api.hitbtc.com/api/3/spot/order').json()
# print('DELETE orders \n: ', clearOrder)
# print('_ _ _ _ _ _ _ _ _ _ _ _ _ ')
# print('_ _ _ _ _ _ _ _ _ _ _ _ _ ')