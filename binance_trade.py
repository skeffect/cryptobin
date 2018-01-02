import sys
import time
import logging
import threading
import json
from pprint import pprint
from binance.client import Client

# Add your API key
api_key = ''
# Add your secret
api_secret = ''
RECV_WINDOW=6000000

logging.basicConfig(level=logging.DEBUG,
                    filename='binance.log',
                    format='%(asctime)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p')


def buy(threshold, symb, delta, total):
  #prev_val = float('inf')
  new_th = threshold
  first = 1
  while True:
    info=m1.bnc.get_all_tickers()
    info_dict = json.loads(json.dumps(info))
    p_symbol = float("inf")
    for item in info_dict:
      if (item.get('symbol') == symb):
        p_symbol = float(item.get('price'))
        print "SS: %.6f" % (p_symbol)
        logging.info("p_symbol: %.6f" % (p_symbol))
    if (p_symbol == float("inf")):
      time.sleep(120)
      continue
    if (first == 1):
      prev_val = p_symbol
      first = 0
      continue
    if (p_symbol > prev_val):
      #print "New %s: %.6f, Prev %s: %.6f" % (symb, p_symbol, symb, prev_val)
      logging.info("New %s: %.6f, Prev %s: %.6f" % (symb, p_symbol, symb, prev_val))
      prev_val = p_symbol
      if (p_symbol > new_th):
        print "Placing an order for symbol %s for quantity %f @%f" % (symb, delta, new_th)
        logging.info("Placing an order for symbol %s for quantity %f @%f" % (symb, delta, new_th))
        t_resp = m1.bnc.create_order(symbol=symb,
                                     side=Client.SIDE_BUY,
                                     type=Client.ORDER_TYPE_MARKET,
                                     price=p_symbol,
                                     quantity=delta)
        pprint(t_resp)
        logging.warning(pprint(t_resp))
        new_th = new_th + 0.2*new_th
        total = total - delta
        sys.exit()
    time.sleep(120)
    if (total < delta):
      logging.info("Exiting thread!")
      sys.exit()

def my_balance():
  pprint(m1.bnc.get_account(recvWindow=RECV_WINDOW))


class Myclient:
  def __init__(self):
    self.bnc = Client(api_key, api_secret)

m1 = Myclient()
#my_balance()

#print "================="
#info = m1.bnc.get_symbol_info('LTCBTC')
#info = m1.bnc.get_order_book(symbol='LTCBTC')
info=m1.bnc.get_all_tickers()
#pprint(info)
#print "================="

conv_ltc2btc = threading.Thread(name='conv_LTC_BTC', target=buy(0.02, "LTCBTC", 0.2, 0.2))
conv_btc2xrp = threading.Thread(name='conv_XRP_BTC', target=buy(0.000130, "XRPBTC", 0.002, 0.02))

# Start 2 threads
conv_ltc2btc.start()
conv_btc2xrp.start()


#buy_btc.join()
conv_ltc2btc.join()
conv_btc2xrp.join()

sys.exit()

#print "================="
# General stuff for debugging
#m = Monitor()
##bal = m.my_balance()
#order = m.bac.get_all_orders(symbol="XRPBTC")
#print(order)
#
##info = m.bac.get_exchange_info()
#
##my_balance()
#
##info = m.bac.get_symbol_info('ETHBTC')
##print(info)
##info = m.bac.get_symbol_info('MIOTA')
##print(info)
## get market depth
##depth = m.bac.get_order_book(symbol='IOTA')
##print(depth)
#
## place market buy order
##order = client.create_order(
##  symbol='BNBBTC',
##  side=Client.SIDE_BUY,
##  type=Client.ORDER_TYPE_MARKET,
##  quantity=100)
#
## get all symbol prices
##prices = client.get_all_tickers()
#
## withdraw 100 ETH
## check docs for assumptions around withdrawals
##from binance.exceptions import BinanceApiException, BinanceWithdrawException
##try:
##  prices = client.get_all_tickers()
##  print("Success")
#
## fetch list of withdrawals
##withdraws = client.get_withdraw_history()
#
## fetch list of ETH withdrawals
##eth_withdraws = client.get_withdraw_history('ETH')
#
## get a deposit address
##address = client.get_deposit_address('BTC)
##process_message(address)
#
## start trade websocket
#  # do something
#
##from binance.websockets import BinanceSocketManager
##bm = BinanceSocketManager(client)
##bm.start_aggtrade_socket(symbol='BNBBTC')
##bm.start()

