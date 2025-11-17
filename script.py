import json
from datetime import timedelta, datetime
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.ticker
import ast

trades = pd.read_csv('eth-btc-trades.csv')
orders = pd.read_csv('eth-btc-orderbooks.csv')
orders['asks'] = orders['asks'].apply(ast.literal_eval)
orders['bids'] = orders['bids'].apply(ast.literal_eval)
trades['timestamp'] = pd.to_datetime(trades['timestamp'])
orders['timestamp'] = pd.to_datetime(orders['timestamp'])

for i, row in orders.iterrows():
    print(len(row['asks']))
    print(len(row['bids']))

def draw_graphs(nrows, ncols, data, side):
    prices = []
    sizes = []
    fig, axes = plt.subplots(nrows, ncols, sharex=True,  sharey=True, figsize=(40,24))
    plt.subplots_adjust(wspace=0.02, hspace=0.04, left=0.02, right=0.99, bottom=0.02, top=0.95)
    plt.suptitle(f"Distribution of {side}-orders sizes depending on price and time of a snapshot (4 lines correspond to 4 snapshots specified in an upper right corner)")
    axes = axes.ravel()
    for i in range(len(orders)):
        axes[i//4].spines['right'].set_visible(False)
        axes[i//4].spines['top'].set_visible(False)
        for j in orders[side][i]:
            prices.append(j['price'])
            sizes.append(j['size'])
        axes[i//4].plot(prices, sizes, alpha=0.4, color='blue', linewidth=0.5, label='actual price of BUY-trades bigger than 10ETH')
        axes[i//4].tick_params(axis='both', which='major', labelsize=6)
        snapshot_number = 0
        if i//4 == (i+1)//4:
            time1 = orders.loc[snapshot_number, "timestamp"]
            time2 = orders.loc[snapshot_number+3, "timestamp"]
            axes[snapshot_number].legend(title=time1.strftime('%m-%d %H:%M')+' - '+time2.strftime('%m-%d %H:%M'), title_fontsize= 5, loc='upper right')
        else:
            snapshot_number += 1
        prices = []
        sizes = []
    axes[47].tick_params(labelsize=6)
    plt.show()

draw_graphs(nrows=8, ncols=6, data=orders, side='asks')
draw_graphs(nrows=8, ncols=6, data=orders, side='bids')
orders_trade16_33_30_deleted = orders[orders.timestamp != '2025-09-03 16:33:30.943424800+00:00']
draw_graphs(nrows=8, ncols=6, data=orders_trade16_33_30_deleted, side='asks')

orders['best_price_asks'] = None
orders['best_price_bids'] = None
orders['average_price_asks'] = None
buy_trades = trades[trades['side'] == 'BUY']
sell_trades = trades[trades['side'] == 'SELL']

asks_price = []
bids_price = []
for _, row in buy_trades.iterrows():
    for i, item in orders.iterrows():
        if (row['timestamp'] - item['timestamp']).seconds == 86399:
            print("time of trade:", row['timestamp'])
            print("time of snapshot:", item['timestamp'])
            print("time interval (should be checked manually due to the split-second difference between the trade-file and the orderbook): 0 or 86399sec")
            print("size of trade:", row['size'], "ETH")
        elif (row['timestamp'] - item['timestamp']).days == 0:
            if (row['timestamp'] - item['timestamp']).seconds <= 10:
                print("time of trade:", row['timestamp'])
                print("time of snapshot:", item['timestamp'])
                print("time interval:", (row['timestamp'] - item['timestamp']).seconds, "sec.")
                print("size of trade:", row['size'], "ETH")
        for j in item['asks']:
           asks_price.append(j['price'])
        orders.loc[i, 'best_price_asks'] = np.min(asks_price)
        orders.loc[i, 'average_price_asks'] = np.mean(asks_price)   
        asks_price = []
        for k in item['bids']:
            bids_price.append(k['price'])
        orders.loc[i, 'best_price_bids'] = np.max(bids_price)
        bids_price = []

print(len(buy_trades))
trades_less_10ETH = buy_trades[buy_trades['size'] <= 10]
trades_bigger_10ETH = buy_trades[buy_trades['size'] > 10]
print(len(trades_less_10ETH))
print(len(trades_bigger_10ETH))                  

fig, ax = plt.subplots(nrows=1, ncols=1,  figsize=(18,12))
plt.suptitle("Price in buy-trades compared to best and average price of asks")
ax.plot(orders['timestamp'], orders['best_price_asks'], color='green', linewidth=0.5, label='best ASK-price from orderbook`s snapshots')
ax.plot(orders['timestamp'], orders['average_price_asks'], color='black', linewidth=0.5, label='average ASK-price from orderbook`s snapshots')
ax.plot(buy_trades_bigger_10ETH['timestamp'], buy_trades_bigger_10ETH['price'], color='red', linewidth=0.5, label='actual price of BUY-trades bigger than 10ETH')
ax.plot(buy_trades_less_10ETH['timestamp'], buy_trades_less_10ETH['price'], color='blue', linewidth=0.5, label='actual price of BUY-trades less than 10ETH')
ax.legend(loc='upper right', fontsize=8)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.set_ylabel('Price, ETH/BTC', fontsize=8)
ax.set_xlabel('Time', fontsize=8)
ax.grid()
ax.tick_params(axis='both', which='major', labelsize=6)
plt.show()
