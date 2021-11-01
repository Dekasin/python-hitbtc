import requests
import threading
from math import floor
import time

# seconds passed since epoch
seconds = time.time()
local_time = time.ctime(seconds)
print("SCRIPT START AT:", local_time)

apiKey = 'MOa7_xGmOzehNkVrOFZDhd2gw4sD3X2M'
secretKey = 'R8eM0vmcpx5OtQl08gdhEoSFzAmUlDYh'
loopInterval = 5
priceBuy = 0.9992
priceSell = 1.0056

usdtPriceBuyMax = 0.9999
usdtPriceSellMin = 1.0034
proPriceBuyMax = 0.000026
proPriceSellMin = 0.000034


session = requests.session()
session.auth = (apiKey, secretKey)

# DELETE /api/3/spot/order

clearOrder = session.delete('https://api.hitbtc.com/api/3/spot/order').json()
print('DELETE orders \n: ', clearOrder)
print('_ _ _ _ _ _ _ _ _ _ _ _ _ ')
print('_ _ _ _ _ _ _ _ _ _ _ _ _ ')

def setInterval(func,time):
    e = threading.Event()
    while not e.wait(time):
        func()

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
    

    usdtPrice = session.get('https://api.hitbtc.com/api/3/public/orderbook/USDTDAI').json()
    bid = usdtPrice['bid']
    ask = usdtPrice['ask']
    i = 0
    while freeDai > 0.02:

       
        priceBuyI = float(bid[i][0])
        buyAmountI = float(bid[i][1])

        if priceBuyI > usdtPriceBuyMax:
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

        if priceSellI < usdtPriceSellMin:
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
    
    # print(freeBtc)
    
    i = 0
    while freeBtc > 0.000005:
        
        # print('bid  =  ', bid)
        # print('ask = ' , ask)

        priceBuyI = float(bid[i][0])
        buyAmountI = float(bid[i][1])
        print('ByyAmount:', buyAmountI, freeBtc,'Price =', priceBuyI, 'i=', i )

        # print('btcPrice:', priceBuyI, buyAmountI,  )
        if priceBuyI > float(ask[0][0]) * 0.98:
            True
        elif (priceBuyI > proPriceBuyMax) and freeBtc * 0.1 > 0.000005 and i <= 2:
            orderData = {'symbol':'PROBTC', 'side': 'buy', 'quantity': (freeBtc * 0.1) / (priceBuyI + 0.00000001), 'price': priceBuyI +0.00000001 }
            r = session.post('https://api.hitbtc.com/api/3/spot/order/', data = orderData)
            freeBtc = freeBtc - (freeBtc * 0.1)* (priceBuyI + 0.00000001)
            
            print('Buy PRO  __MIN__0.1__', r.json())
            print('FREE BTC_______', freeBtc)
            print('_______')
            showTime()
            getBalance()

        elif (priceBuyI > proPriceBuyMax)  and i > 2:
            False


        elif buyAmountI < freeBtc / priceBuyI:
            orderData = {'symbol':'PROBTC', 'side': 'buy', 'quantity': buyAmountI, 'price': priceBuyI +0.00000001 }
            r = session.post('https://api.hitbtc.com/api/3/spot/order/', data = orderData)
            freeBtc = freeBtc - buyAmountI * (priceBuyI + 0.00000001)
            
            print('Buy PRO  min', r.json())
            print('_______')
            showTime()
            getBalance()
    
        else:
            orderData = {'symbol':'PROBTC', 'side': 'buy', 'quantity': freeBtc / (priceBuyI + 0.00000001), 'price': priceBuyI + 0.00000001 }
            r = session.post('https://api.hitbtc.com/api/3/spot/order/', data = orderData)
            
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

    while freePro > 0.1:
               
        priceSellI = float(ask[i][0])
        sellAmountI = float(ask[i][1])

        if priceSellI < float(bid[0][0]) * 1.02:
            True
        elif (priceSellI < proPriceSellMin) and freePro * 0.1 > 0.1 and i <= 2:
            # True
            orderData = {'symbol':'PROBTC', 'side': 'sell', 'quantity': freePro * 0.1, 'price': priceSellI -0.000000001 }
            r = session.post('https://api.hitbtc.com/api/3/spot/order/', data = orderData)
            
            freePro -= (freePro * 0.1)
            print('Sell PRO __MIN___0.1__', r.json())
            print('Order data',orderData)
            print("freePRO", freePro)
            print('_______')
            showTime()
            getBalance()

        elif (priceSellI < proPriceSellMin) and i > 2:
            True    

        elif sellAmountI < freePro:
            orderData = {'symbol':'PROBTC', 'side': 'sell', 'quantity': sellAmountI, 'price': priceSellI - 0.000000001 }
            r = session.post('https://api.hitbtc.com/api/3/spot/order/', data = orderData)
           
            freePro -= sellAmountI
            print('Sell PRO', r.json())
            print('Order data',orderData)
            print("freePRO", freePro)
            print('_______')
            showTime()
            getBalance()
    
        else:
            orderData = {'symbol':'PROBTC', 'side': 'sell', 'quantity': freePro, 'price': priceSellI -0.000000001 }
            r = session.post('https://api.hitbtc.com/api/3/spot/order/', data = orderData)
            
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
setInterval(loop,loopInterval)
