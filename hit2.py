import requests
import threading
from math import floor

apiKey = 'wYt_9D5jNJV7OTza9Dhp9Kx0vb3IHIUw'
secretKey = 'vwoLUogDZHxcaEsg-iuyh66EH33HjpD4'
loopInterval = 5

session = requests.session()
session.auth = (apiKey, secretKey)

def loop():
    
    usdt = session.get('https://api.hitbtc.com/api/3/public/orderbook/USDTDAI').json()

    ask = usdt['ask']
    bid = usdt['bid']

    print(ask[0][0], bid[0][0])

   
    
loop()
