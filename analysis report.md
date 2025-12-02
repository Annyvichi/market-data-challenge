# Market Data Analysis Report 

## Key Findings

### Anomaly with bids- and asks-lists in the Orderbook.
The first acquaintance with the orderbook shows that the length of bids- and asks-lists is the same in every snapshot and is always equal to 50. It looks like it's a truncated version of the orderbook, otherwise it would be very strange.

### The orderbook does not reflect the actual trading volume on the market.
Visual assessment of distribution of bid- and ask-orders shows that almost all of the orderbook's asks are close to 0, there is only one exeption - on the penultimate graph. 
![picture 1: Distribution of ask-orders sizes](orderbook_ask_distribution.png)
![picture 2: Distribution of bid-orders sizes](orderbook_bid_distribution.png)
This exeption can be found in the 6th from the end snapshot: '2025-09-03 16:33:30.943424800 ... {'price': 0.03984, 'size': 199.665}, ...'
After looking for it in the 'eth-btc-trades.csv' it was found out that this aks-order was bought at exactly 16:33:30 - the same minute and second it was placed in the orderbook.
It can be seen at the next picture how the ask-distribution looks when '16:33:30'-snapshot is deleted.
![picture 3: Distribution of ask-orders sizes with '16:33:30'-snapshot deleted](orderbook_ask_distr_16_33deleted.png)

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

It turns out almost all buy-trades exceeding 10 ETH are out the snapshots (all but the abovementioned '16:33:30'-trade). 

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

The 4th transaction was made in less than 2 seconds after creating an ask-order, because there is no ask-order of this size in the 07:23:18-snapshot. The 1st, 2nd and 3rd transactions were made in less than 7 - 8 seconds.

The conclusion of this paragraph is: the prevailed majority of buy-trades was most likely executed within seconds or splits of seconds after placing orders.

### Price in buy-trades against the best and average ask-price from orderbook's snapshots.
If 677 out of 678 buy-transactions exceeding 10ETH were executed so quickly that they were out of the orderbook's snapshots the quiestion is: what was their price? Was it always the best price?
The picture below shows the best (green line) and the average (blue line) ask-price from the orderbook's snapshots against the actual price of the buy-trades (red lines).
![picture 4: Price in buy-trades compared to best and average ask-price from snapshots](price.png)
The actual buy-price is really better than what can be seen in the orderbook's snapshots most of the time. Which can be a normal market behaviour, though it looks like guys with the best price are always so close... It seems reasonable to check the rest ask-prices. But the suspicious part here is this: if selling ETH was so successful that all huge offers were bought so quickly, why not to try to sell it at a higher price - place an order into the orderbook and wait for a while? Not even once out of 678 times?

### Ask- and bid-prices from orderbook's snapshots compared to each other.
To explore the premice from the previous paragraph, all 50 asks and 50 bids (as it was mentioned in the beginning the lenght of orderbook's lists is 50) at every timestamp were visualized. The lowest ask-line (light blue) is the best ask-price at different timestampes, the highest ask-line is the least competitive ask-price. And it's vice versa with the bid-lines (yellow).
![picture 5: Bid-prices against the actual sell-price](bid-prices.png)

It can be seen that ask-lines and bid-lines shift relative to some level from time to time, almost all of them. It is because the majority of asks and bids is mostly the same, so for example when a new ask is added to a list which is almost the same (or removed from a list) - all higher ask-offers shift on one level.
But ask- and bid-lines shift back to the same levels from time to time as well.

To explain this observation it is interesting to consider the following asks from three snapshots:
2025-09-02 14:54:24 ... {'price': 0.04192, 'size': 0.00024652}, {'price': 0.04197, 'size': 0.00024694}, {'price': 0.04197577, 'size': 0.01199991}, {'price': 0.042, 'size': 0.00474414}, {'price': 0.04202, 'size': 0.00023971}, {'price': 0.04207, 'size': 0.00023942}, {'price': 0.0421, 'size': 0.0025}, ... 

2025-09-03 03:07:03 ... {'price': 0.04192, 'size': 0.00024652}

2025-09-03 19:55:17 ... {'price': 0.04192, 'size': 0.00024652}, {'price': 0.04197, 'size': 0.00024694}, {'price': 0.04197577, 'size': 0.01199991}, {'price': 0.04199, 'size': 0.00027}, {'price': 0.042, 'size': 0.00474414}, {'price': 0.04202, 'size': 0.00023971}, {'price': 0.04207, 'size': 0.00023942}, {'price': 0.0421, 'size': 0.0025}

This part "{'price': 0.04192, 'size': 0.00024652}" is common for every timestamp. But for 03:07 timestamp it is the ending (the last 50th ask). Whereas in 14:54 timestamp there are higher price levels. And at 19:55 these levels are back again. Actually not just price levels but  absolutely identical asks: {'price': 0.04197, 'size': 0.00024694}, {'price': 0.04197577, 'size': 0.01199991}, {'price': 0.042, 'size': 0.00474414}, {'price': 0.04202, 'size': 0.00023971}, {'price': 0.04207, 'size': 0.00023942}, {'price': 0.0421, 'size': 0.0025}.

It is unlike normal market behaviour, but it is very likely that this is the part where the orderbook was truncated: from the ending of the lists.

Bid-prices from snapshots:
2025-09-01 03:52:04 ... {'price': 0.0377, 'size': 0.00311485}, {'price': 0.03763159, 'size': 0.02189266}, {'price': 0.0376, 'size': 0.00438429}]"

2025-09-01 05:05:14 ... {'price': 0.0377, 'size': 0.00311485}]"

2025-09-01 08:07:49 ... {'price': 0.0377, 'size': 0.00311485}, {'price': 0.03763159, 'size': 0.02189266}]"

2025-09-01 14:32:14 ... {'price': 0.0377, 'size': 0.00311485}, {'price': 0.03763159, 'size': 0.02189266}, {'price': 0.0376, 'size': 0.00438429}, {'price': 0.03759, 'size': 0.00205824}]"
The list is truncated at 05:05 and partially at 08:07-snapshot, but at 03:52 and 14:32 longer versions can be seen.
The same pattern can be observed at picture 5 between September 1 11p.m. and September 2 02a.m., also on September 2 between 06a.m. and 01p.m.(I checked the lists - they are truncated in the same way). So bid-lists the same as ask-lists are truncated from the ending.

There is another pattern at the initial parts of the bid-lists, which I think contradicts normal market behaviour: 
2025-09-02 14:36:07 ... {'price': 0.03939782, 'size': 0.00229782}, {'price': 0.0393, 'size': 0.00261679}, {'price': 0.03925777, 'size': 0.00246826}, {'price': 0.0392, 'size': 0.00287474}, {'price': 0.0391, 'size': 0.0028757}, {'price': 0.03907353, 'size': 0.04093716}, {'price': 0.03900577, 'size': 0.01444284}, 
{'price': 0.0390001, 'size': 0.00027}, ... 
{'price': 0.0389, 'size': 0.00287763}, {'price': 0.03885, 'size': 0.00025997}...

2025-09-03 03:25 {'price': 0.0390001, 'size': 0.00027}, ... {'price': 0.0389, 'size': 0.00287763}, {'price': 0.03885, 'size': 0.00025997}...

2025-09-03 15:56 ... {'price': 0.03939782, 'size': 0.00230517}, {'price': 0.0393, 'size': 0.00254605}, {'price': 0.03925777, 'size': 0.00247084}, {'price': 0.0392, 'size': 0.00255229}, {'price': 0.0391, 'size': 0.00255882}, 
{'price': 0.0389, 'size': 0.00025964}, {'price': 0.03885, 'size': 0.00025997}...

At 03:25 the best bid-price is low - the market price was low at that timestamp, so bid price dropped either, but in the last snapshot (when market price recovered) the prices from the first snapshot are back.

Comparing snapshots on a longer timeframe shows that more removed bid-prices were restored:
2025-09-01 20:01:09 ... {'price': 0.0398, 'size': 0.00251407}, {'price': 0.0397, 'size': 0.0025204}, {'price': 0.03968253, 'size': 0.00293983}, {'price': 0.0395, 'size': 0.0026162}, {'price': 0.0394, 'size': 0.01482199}, 
{'price': 0.03939782, 'size': 0.00229782}, {'price': 0.0393, 'size': 0.00261679}, {'price': 0.03925777, 'size': 0.00246826}, {'price': 0.0392, 'size': 0.00287474}, {'price': 0.0391, 'size': 0.0028757}, {'price': 0.03907353, 'size': 0.04093716}, {'price': 0.03900577, 'size': 0.01444284}, {'price': 0.0390001, 'size': 0.00027}, {'price': 0.039, 'size': 0.00287435}, 
{'price': 0.0389, 'size': 0.00287763}, {'price': 0.03885, 'size': 0.00025997}...

2025-09-03 20:50:36 {'price': 0.0398, 'size': 0.0032}, {'price': 0.0397, 'size': 0.0032}, {'price': 0.0396, 'size': 0.00688878}, {'price': 0.03950495, 'size': 0.0032}, 
{'price': 0.03939782, 'size': 0.00230517}, {'price': 0.0393, 'size': 0.00254605}, {'price': 0.03925777, 'size': 0.00247084}, {'price': 0.0392, 'size': 0.00255229}, {'price': 0.0391, 'size': 0.00255882}, 
{'price': 0.0389, 'size': 0.00025964}, {'price': 0.03885, 'size': 0.00025997}...

One more example from September 3 morning, when buying price dropped and recovered:
2025-09-03 07:23:18.802576200+00:00  ... {'price': 0.0389, 'size': 0.00287763}, {'price': 0.03885, 'size': 0.00025997}, 
{'price': 0.0388, 'size': 0.01061054}, {'price': 0.0387, 'size': 0.00287958},

2025-09-03 07:41:41 {'price': 0.0388, 'size': 0.00365465}, {'price': 0.0387, 'size': 0.00287958},

2025-09-03 10:26:40 {'price': 0.0391, 'size': 0.00077489}, {'price': 0.0389, 'size': 0.00025964}, {'price': 0.03885, 'size': 0.00025997}, {'price': 0.0388, 'size': 0.00151792}... 

It is strange that many bids were placed at the same price levels after previous removing.

### Simultaneous changes in bid- and ask-lists.
One more strange pattern was noticed: there are 9 significant simultaneous shifts of bid- and ask-lines (picture 5). 6 of them can be caused by a significant market price change. But at least 3 simultaneous shifts (at around 4a.m, between 1p.m. - 2p.m. and at around 5 p.m. on September 1) can't be explained by the market price movement, because there are less significant price changes at these timestamps than at many other ones.

## Conclusion
My suggestion is it was artificial trading and orderbook manipulation.