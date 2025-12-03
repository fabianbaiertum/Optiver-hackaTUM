# Optiver-hackaTUM
In November 2025, my team had the 3rd highest PnL at the hackaTUM in Munich (even with major errors during the final run). Here, I describe the challenge and my approach in a simplified way to ensure fairness in future competitions.
I designed all the strategies and how to combine them myself, as well as the execution logic. My teammates threaded it, used the API to get the data from the Optibook and wrote the final version, combining the strategies elegantly. 

## The challenge
The trading took place on Optiver's Optibook, a simulated exchange where there are bots and other teams with whom we could trade. It is a simplified version of a real market, e.g. prices are close to a symmetric random walk, unless news for that specific stock appear. Overall, there were 5 different stocks with their dual listings available. So it was quite clear from the beginning that I wanted to do statistical arbitrage, market making and news-based directional trading. The main challenge was to classify the incoming news and decide which of the 5 stocks would be affected and either positively, neutral or negatively and then trade in this direction (of course, also affecting the dual listing). For the time, when no news is incoming for a specific stock, we would do market making, and if there exists an arbitrage opportunity, capture it. At the end, I combined those strategies to run in parallel.

There was a limit of 25 (inserts, amends or cancels) per second. 

## News-based directional sentiment trading
At a random time, there could come some news, which may affect any stock either positively or negatively. We used an LLM-based model to classify for one specific news, which stocks are affected how intense the effect will be. Also, if, for example, we classified that the Nvidia stock is going to rise due to this news item, we would go long in the primary listing as well as the dual listing. 

## Statistical arbitrage
For the dual listing, I had a strategy as soon as the prices diverged: we bought the cheaper of them and sold the more expensive one and vice versa. We had this running for all 5 different stocks in parallel, checking if there were any statistical arbitrage opportunities. We took the liquidity of the two exchanges into account and decided which volume we should post; If we were holding a position from market making on the wrong side of the predicted price movement, we would want a higher execution probability.
After entering the trade, we would wait until the prices converged and closed all of the volume we hold in each (i.e. the stock primary and its dual listings positions).
Also, if only the microprices differ, we could take a slightly shifted microprice for our market making algorithm as input.

## Market making
For the market making of each stock, I used an improved version of my IMC prosperity and the last Optiver hackathon (1st place). It takes into account market microstructure signals, which are relevant in the Optibook.
I split it into three modules: pricing, execution and position sizing.
The pricing module outputs theoretical prices at which we should place our orders.
The execution module takes queue priority, tick sizes and where other market makers quote into account.
The position sizing module decides how much volume we want to post at each side.
One challenge was to decide when to cancel, amend or insert limit orders. As far as I know, no other team in the competition considered this in their final algorithm, giving us queue priority over them.


Email me for the full code if you are a recruiter from a quantitative trading firm.
