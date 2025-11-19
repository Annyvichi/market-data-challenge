# Market Data Analysis Report 

## Key Findings

### Anomaly with bids- and asks-lists in the Orderbook.
The first acquaintance with the orderbook shows that the length of bids- and asks-lists is the same in every snapshot and is always equal to 50. If there is no any limit on the length, it raises suspicion.

### Orderbook is too different from what was happenning on the buy-side of the market.
Visual assessment of distribution of bid- and ask-orders shows that almost all of the orderbook's asks are close to 0, there is only one exeption - on the penultimate graph. 
![Distribution of ask-orders sizes](orderbook_ask_distribution.png)
![Distribution of bid-orders sizes](orderbook_bid_distribution.png)
This exeption can be found in the 6th from the end snapshot: '2025-09-03 16:33:30.943424800 ... {'price': 0.03984, 'size': 199.665}, ...'
After looking for it in the 'eth-btc-trades.csv' it was found out that this aks-order was bought at exactly 16:33:30 - the same minute and second it was placed in the orderbook.
It can be seen at the next picture how the ask-distribution looks when '16:33:30'-snapshot is deleted.
![Distribution of ask-orders sizes with '16:33:30'-snapshot deleted](orderbook_ask_distr_16_33deleted.png)

The next step was checking the max-values of buy- and sell-trades as well as their distribution.
There were 720 BUY-trades and 125 sell-trades totally.

max sell-trade: 0.19106776 ETH;  total volume of sell-trades: 0.9603567500000002 ETH
max buy-trade: 687.32918 ETH;  total volume of buy-trades: 168297.80241572 ETH

The total volume of sell-trades is insignificant, what can be interesting is the distribution of buy-trades:

number of buy-trades less than 0.01ETH: 36 , volume: 0.04649978
number of buy-trades between 0.01 - 0.1ETH: 5 , volume: 0.08919394
number of buy-trades between 0.1 - 1ETH: 0 , volume: 0.0
number of buy-trades between 1 - 10ETH: 1 , volume: 7.485598
number of buy-trades between 10 - 100ETH: 152 , volume: 9824.763454
number of buy-trades exceeding 100ETH: 526 , volume: 158465.41767

For simplicity the total volume of buy-trades was divided into two main groups - transactions less than 10EHT and transactions exceeding 10ETH:

number of buy-trades less than 10ETH: 42 , volume: 7.62129172
number of buy-trades exceeding 10ETH: 678 , volume: 168290.181124

It turns out almost all these buy-trades exceeding 10 ETH are out the snapshots (all but the abovementioned '16:33:30'-trade). 

Then it is necessary to check whether there were other similar cases, for example, when a snapshot was taken less than 10 seconds before a buy-trade of over 10 ETH was carried out. 
4 cases were discovered:

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

The 4th transaction was made in less than 2 seconds after creating an ask-order, because there is no bid-order of this size in the followed snapshot. The 1st, 2nd and 3rd transactions were made in less than 7 - 8 seconds.

The conclusion of this paragraph is: the prevailed majority of buy-trades was most likely executed within seconds or splits of seconds after placing orders.

### Price
If 677 out of 678 buy-transactions exceeding 10ETH were executed so quickly that they were out of the orderbook's snapshots the quiestion is: what was their price? Was it always the best price?
The picture below shows the best (green line) and the average (blue line) ask-price from the orderbook's snapshots against the actual price of the buy-trades (red lines).
![Price in buy-trades compared to best and average ask-price from snapshots](price.png)
So the actual buy-price is really better than what can be seen in the orderbook's snapshots most of the time. Which is what it should be like. But the suspicious part is - there were 678 buy-trades exceeding 10ETH (thin red line), their price is almost always the best price or very close to it and none of them had a price close to the average ask-prise.

## Conclusion
My suggestion is it was artificial trading. Probably wash trading, then part of the buy-volume, maybe most of it can be fake.