# Market Data Analysis Report 

## Key Findings

### Anomaly with bids- and asks-lists in the Orderbook.
1. The first acquaintance with the orderbook shows that the length of bids' and asks' lists is the same in every snapshot and is always equal to 50. If there is no any limit on the length, it looks suspicious.

### Orderbook is too different from what was happenning on the BUY-side of the market.
2. Visual assessment of distribution of bid- and sell-orders reveals another obvious anomaly: almost all of the orderbook's asks are close to 0, there is only one exeption - on the penultimate graph. 
![Distribution of ask-orders sizes](orderbook_ask_distribution.png)
![Distribution of bid-orders sizes](orderbook_bid_distribution.png)
This exeption can be found in the 6th from the end snapshot: '2025-09-03 16:33:30.943424800+00:00,"{'price': 0.03984, 'size': 199.665}, ..."
After looking for it in the 'eth-btc-trades.csv' we find out that this aks-order was bought at exactly 16:33:30 - the same minute and second it was placed in the orderbook.
It can be seen at the next picture how the ask-distribution looks when '2025-09-03 16:33:30.943424800+00:00'-snapshot is deleted.
![Distribution of ask-orders sizes] ('2025-09-03 16:33:30.943424800+00:00'-snapshot is deleted)](orderbook_ask_distribution.png)

The next step was checking the distribution of BUY-trades in the 'eth-btc-trades.csv'. There were 720 BUY-trades:
"print(len(buy_trades))
720"
and only 42 of them are less than 10ETH:
"print(len(trades_less_10ETH))
42"

Which means almost all the BUY-trades bigger than 10 ETH are out the snapshots (all but the '2025-09-03 16:33:30'-trade). So the trades-file and the orderbook were checked on the presence of other similar events when a shapshot was taken in less than 10 seconds after a BUY-trade. 
4 events of that kind were discovered:

time of trade: 2025-09-02 01:11:34+00:00
time of snapshot: 2025-09-02 01:11:25.228272300+00:00
time interval: 8 sec.
size of trade: 510.516 ETH

time of trade: 2025-09-02 02:06:15+00:00
time of snapshot: 2025-09-02 02:06:07.126520700+00:00
time interval: 7 sec.
size of trade: 323.52829 ETH

time of trade: 2025-09-02 07:34:59+00:00
time of snapshot: 2025-09-02 07:34:51.396485700+00:00
time interval: 7 sec.
size of trade: 27.151483 ETH

time of trade: 2025-09-03 07:23:21+00:00
time of snapshot: 2025-09-03 07:23:18.802576200+00:00
time interval: 2 sec.
size of trade: 119.4285 ETH

The 4th transaction was made in less than 2 sec. after creating an ask-order, because there is no bid-order of this size in the followed snapshot. The 1st, 2nd and 3rd transactions were made in less than 7 - 8 sec.

The conclusion of this paragraph is: the prevailed majority of BUY-trades was most likely executed within seconds or splits of seconds after placing orders.

### Price
3. If 677 out of 678 BUY-transactions bigger that 10ETH were executed so quickly that they were not included the orderbook's snapshots the quiestion is: what was their price? Was it always the best price?
There is the representation of the best offer from the orderbook against the actual price of the BUY-trades bigger than 10 ETH:
![Price in buy-trades compared to best and average price of asks](price.png)
So their actual BUY-price is really better than what can be seen in the orderbook most of the time. It also can be noticed that the line corresponding to actual price is more curved compared to the orderbook's best price line, so there were many better offers. A couple of a few exceptions can be seen in the interval between 18 and 20 hours on September 2, when the actual price was higher than the best price from the orderbook, but anyway it was far from the average ask-price and those orders were bougt very quickly. So there were 678 BUY-trades bigger than 10ETH and none of them had a price close to the average ask-prise. Looks suspicious. 

## Conclusion
My suggestion is the situation described here is artificial trading. It could be wash trading when fake volume was created.