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
    plt.suptitle(f"Distribution of {side} sizes depending on price (4 lines correspond to 4 snapshots specified in an upper right corner)")
    axes = axes.ravel()
    for i in range(len(data)):
        axes[i//4].spines['right'].set_visible(False)
        axes[i//4].spines['top'].set_visible(False)
        for j in data[side][i]:
            prices.append(j['price'])
            sizes.append(j['size'])
        axes[i//4].plot(prices, sizes, alpha=0.4, color='blue', linewidth=0.5, label=data.loc[i, "timestamp"].strftime('%m-%d %H:%M'))
        axes[i//4].legend(fontsize= 5, loc='upper right')
        axes[i//4].tick_params(axis='both', which='major', labelsize=6)
        prices = []
        sizes = []
    axes[47].tick_params(labelsize=6)
    plt.show()

draw_graphs(nrows=8, ncols=6, data=orders, side='asks')
draw_graphs(nrows=8, ncols=6, data=orders, side='bids')
orders_trade16_33deleted = orders[orders.timestamp != '2025-09-03 16:33:30.943424800+00:00']
orders_trade16_33deleted = orders_trade16_33deleted.reset_index(drop=True)
print(orders['asks'][181:])
print(orders_trade16_33deleted['asks'][181:])
draw_graphs(nrows=8, ncols=6, data=orders_trade16_33deleted, side='asks')

buy_trades = trades[trades['side'] == 'BUY']
sell_trades = trades[trades['side'] == 'SELL']
print("max sell-trade:", np.max(sell_trades['size']), "ETH; ", "total volume of sell-trades:", np.sum(sell_trades['size']), "ETH")
print("max buy-trade:", np.max(buy_trades['size']), "ETH; ", "total volume of buy-trades:", np.sum(buy_trades['size']), "ETH")

buy_trades_less_001ETH = buy_trades[buy_trades['size'] <= 0.01]
buy_trades_between001_01ETH = buy_trades[(buy_trades['size'] <= 0.1) & (buy_trades['size'] > 0.01)]
buy_trades_between01_1ETH = buy_trades[(buy_trades['size'] <= 1) & (buy_trades['size'] > 0.1)]
buy_trades_between1_10ETH = buy_trades[(buy_trades['size'] <= 10) & (buy_trades['size'] > 1)]
buy_trades_between10_100ETH = buy_trades[(buy_trades['size'] <= 100) & (buy_trades['size'] > 10)]
buy_trades_more100ETH = buy_trades[buy_trades['size'] > 100]
print("number of buy-trades less than 0.01ETH:", len(buy_trades_less_001ETH), ", volume:", np.sum(buy_trades_less_001ETH['size']))
print("number of buy-trades between 0.01 - 0.1ETH:", len(buy_trades_between001_01ETH), ", volume:", np.sum(buy_trades_between001_01ETH['size']))
print("number of buy-trades between 0.1 - 1ETH:", len(buy_trades_between01_1ETH), ", volume:", np.sum(buy_trades_between01_1ETH['size']))
print("number of buy-trades between 1 - 10ETH:", len(buy_trades_between1_10ETH), ", volume:", np.sum(buy_trades_between1_10ETH['size']))
print("number of buy-trades between 10 - 100ETH:", len(buy_trades_between10_100ETH), ", volume:", np.sum(buy_trades_between10_100ETH['size']))                  
print("number of buy-trades exceeding 100ETH:", len(buy_trades_more100ETH), ", volume:", np.sum(buy_trades_more100ETH['size']))

buy_trades_less_10ETH = buy_trades[buy_trades['size'] <= 10]
buy_trades_exceeding_10ETH = buy_trades[buy_trades['size'] > 10]
print("number of buy-trades less than 10ETH:", len(buy_trades_less_10ETH), ", volume:", np.sum(buy_trades_less_10ETH['size']))
print("number of buy-trades exceeding 10ETH:", len(buy_trades_exceeding_10ETH), ", volume:", np.sum(buy_trades_exceeding_10ETH['size']))

orders['best_price_asks'] = None
orders['best_price_bids'] = None
orders['average_price_asks'] = None
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

fig, ax = plt.subplots(nrows=1, ncols=1,  figsize=(18,12))
plt.suptitle("Price in buy-trades compared to best and average ask-price from snapshots")
ax.plot(buy_trades_exceeding_10ETH['timestamp'], buy_trades_exceeding_10ETH['price'], color='red', linewidth=0.4, alpha=0.7, label='actual price of BUY-trades exceeding 10ETH')
ax.plot(buy_trades_less_10ETH['timestamp'], buy_trades_less_10ETH['price'], color='red', linewidth=0.7, label='actual price of BUY-trades less than 10ETH')
ax.plot(orders['timestamp'], orders['best_price_asks'], color='green', linewidth=0.5, label='best ASK-price from orderbook`s snapshots')
ax.plot(orders['timestamp'], orders['average_price_asks'], color='blue', linewidth=0.5, label='average ASK-price from orderbook`s snapshots')
ax.legend(loc='upper right', fontsize=8)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.set_ylabel('Price, ETH/BTC', fontsize=8)
ax.set_xlabel('Time', fontsize=8)
ax.grid()
ax.tick_params(axis='both', which='major', labelsize=6)
plt.show()
