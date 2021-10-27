import threading
from math import floor 

# API Key: p54r5jlFe00RyRIs3-qHBfVsWPPcJN2z
# Secret Key: Wb_3e0kN7AIi1LlzCTCv8eSK4LZNjtBA

# Sub
# API Key: MOa7_xGmOzehNkVrOFZDhd2gw4sD3X2M
# Secret Key: R8eM0vmcpx5OtQl08gdhEoSFzAmUlDYh

def setInterval(func,time):
    e = threading.Event()
    while not e.wait(time):
        func()

b = {'available': '15.877036568500', 'reserved': '0', 'reserved_margin': '0'}
amountUsdt = float(b['available'])
c = floor(amountUsdt*100)/100
print (c)

# def foo():
#     if b[available] > 0.2:
    
#         print ("hello")

# using
#setInterval(foo,5)