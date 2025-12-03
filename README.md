# Optiver-hackaTUM
In November 2025, our team had the 3rd highest PnL at the hackaTUM in Munich (even with major errors during the final run). Here, we describe the challenge and our approach in a simplified way to ensure fairness in future competitions.

## The challenge
The trading took place on Optiver's Optibook, a simulated exchange where there are bots and other teams with whom we could trade. It is a simplified version of a real market, e.g. prices are close to a symmetric random walk, unless news for that specific stock appear. Overall, there were 5 different stocks with their dual listings available. So it was quite clear from the beginning that we wanted to do statistical arbitrage and news-based directional trading. The main challenge was to classify the incoming news and decide which of the 5 stocks would be affected and either positively, neutral or negatively and then trade in this direction (of course, also affecting the dual listing). For the time, when no news is incoming for a specific stock, we would do market making, and if there exists an arbitrage opportunity, capture it. At the end, we combined those strategies to run in parallel.

## News-based directional sentiment trading

## Statistical arbitrage
For the dual listing, we had a strategy as soon as the prices diverged, we bought the cheaper of them and sold the more expensive one and vice versa. We had this running for all 5 different stocks in parallel, checking if there were any statistical arbitrage opportunities. We took the liquidity of the two exchanges into account and decided which volume we should post; If we were holding a position from market making on the wrong side of the predicted price movement, we would want a higher execution probability.
After entering the trade, we would wait until the prices converged and closed all of the volume we hold in each (i.e. the stock primal and its dual listings positions).
Also, if only the microprices differ, we could take a slightly shifted microprice for our market making algorithm as input.

## Market making



