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
- Risk Management: If we predicted wrong, we would detect it after a short delay and close out the position.
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

For each stock we ran a **microstructure-driven market making strategy**, based on my previous work from IMC Prosperity and Optiver hackathon (including a **1st place** result).

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
     - Strength of signals (e.g. imbalance, news, stat-arb opportunities)

A key edge was **explicitly reasoning about queue priority and rate limits**.  
As far as I know, most teams did not systematically optimize cancel/amend/insert decisions, which gave us **better execution priority**.

---

## Strategy integration and orchestration

All three strategy families ran **in parallel**:

- **News trading** drove directional exposure when strong signals were present
- **Stat-arb** continuously monitored cross-venue mispricings
- **Market making** provided background liquidity and captured spread

I designed the **combination logic**.

For the future, we could take this into account:

- Resolve conflicts between strategies (e.g. news vs. stat-arb) based on:
  - Signal strength
  - Inventory
  - Risk budget
- Centralize **rate-limit management** so high-value actions (e.g. news or stat-arb fills)  
  could temporarily pre-empt less critical market-making updates.

---

## Code availability

The full codebase includes:

- Strategy logic (pricing, risk, signal integration)
- Execution and queue-priority handling
- Monitoring and basic diagnostics

> **If you are a recruiter from a quantitative trading firm**, feel free to email me for access to the full implementation and additional technical details.
