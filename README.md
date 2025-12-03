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


# Optiver-hackaTUM

In November 2025, my team achieved the **3rd highest PnL** at Optiver’s hackaTUM in Munich (despite major errors during the final run).  
This write-up is intentionally simplified to keep the challenge fair for future participants and focuses on the **quantitative / engineering aspects** of my contribution.

I **designed all trading strategies, the combination logic, and the execution layer**.  
My teammates focused on threading, data ingestion from Optibook’s API, and integrating my strategies into a clean final architecture.

---

## The challenge

The competition ran on **Optiver’s Optibook**, a simulated exchange with bots and other teams as counterparties.  
Prices approximately followed a **symmetric random walk**, except when **idiosyncratic news** arrived for a given stock.

- Universe: **5 stocks**, each with a **dual listing**
- Objective: maximize **PnL** under realistic microstructure constraints
- Key constraint: **25 order operations per second** (inserts, amends, cancels)

From the problem structure it was clear that a competitive solution should combine:

- **Market making**
- **Statistical arbitrage** between primary and dual listings
- **News-based directional trading**

The core difficulty was to **map incoming news to the affected stock(s)**, determine **direction and magnitude** of the impact, and integrate this with market making and stat-arb under a strict **rate limit**.

---

## News-based directional sentiment trading

At random times, news items arrived that could affect any subset of the 5 stocks positively or negatively.

- Used an **LLM-based classifier** to map each news item to:
  - Relevant stock(s)
  - Direction (**long/short/neutral**)
  - Confidence / intensity of impact
- When, for example, news indicated a **positive signal for NVIDIA**:
  - Opened **long positions** in both the **primary listing and the dual listing**
  - Adjusted exposure based on confidence score and current inventory
- Integrated this with the execution layer so that **news-driven orders respected rate limits**.

---

## Statistical arbitrage between dual listings

For each stock, we continuously monitored the **spread between primary and dual listings**.

- When prices diverged beyond a threshold:
  - **Longed the cheaper** listing and **shorted the richer** one
  - Took into account **available liquidity** on both venues to size positions
- If we were holding inventory from market making on the “wrong” side of predicted movement,  
  we **increased execution priority** for mean-reverting trades.
- Exit logic:
  - Waited for **convergence of prices** and then flattened both legs
- We also used **microprice differences** as an additional signal:
  - If only microprices diverged, we **nudged the theoretical prices** for the market making component accordingly.

---

## Market making with microstructure signals

For each stock we ran a **microstructure-driven market making strategy**, based on my previous work from IMC Prosperity and Optiver hackathons (including a **1st place** result).

The market-maker was split into three modules:

1. **Pricing module**  
   - Produced **theoretical bid/ask levels** using:
     - Order book imbalance
     - Microprice
     - Short-term volatility
     - Inventory risk adjustments

2. **Execution module**  
   - Translated theoretical prices into **actual limit orders** while:
     - Explicitly modeling **queue priority**
     - Respecting **tick size** and existing quotes from other market makers
     - Prioritizing **amend vs cancel vs insert** under the **25 ops/sec** limit

3. **Position sizing module**  
   - Determined **volume per side** based on:
     - Current inventory
     - Recent PnL volatility
     - Strength of signals (e.g. imbalance, news, stat-arb opportunities)

A key edge was **explicitly reasoning about queue priority and rate limits**.  
As far as I know, most teams did not systematically optimize cancel/amend/insert decisions, which gave us **better execution priority** at similar quoted spreads.

---

## Strategy integration and orchestration

All three strategy families ran **in parallel**:

- **News trading** drove directional exposure when strong signals were present
- **Stat-arb** continuously monitored cross-venue mispricings
- **Market making** provided background liquidity and captured spread

I designed the **combination logic**, which:

- Resolved conflicts between strategies (e.g. news vs. stat-arb) based on:
  - Signal strength
  - Inventory
  - Risk budget
- Centralized **rate-limit management** so high-value actions (e.g. news or stat-arb fills)  
  could temporarily pre-empt less critical market-making updates.

---

## Code availability

The full codebase includes:

- Strategy logic (pricing, risk, signal integration)
- Execution and queue-priority handling
- Monitoring and basic diagnostics

> **If you are a recruiter from a quantitative trading firm**, feel free to email me for access to the full implementation and additional technical details.
