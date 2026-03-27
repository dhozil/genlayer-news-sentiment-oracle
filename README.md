# 📰 Build a News Sentiment Oracle on GenLayer — Tutorial

What we’re building: An Intelligent Contract that fetches live news, analyzes sentiment, and stores the result on-chain — all without a centralized oracle.

Why this is powerful: Traditional smart contracts cannot read news. GenLayer contracts can — and multiple AI validators independently verify the sentiment before reaching consensus.

-----

## Prerequisites

- GenLayer Studio account at [studio.genlayer.com](https://studio.genlayer.com)
- Connected to Testnet Bradbury
- Test GEN tokens (use the Faucet)

-----

## Step 1: Create the Contract

Open Studio → click ”+” → name it news_sentiment_oracle.py

Paste this code:
# v0.1.0
# { "Depends": "py-genlayer:15qfivjvy80800rh998pcxmd2m8va1wq2qzqhz850n8ggcr4i9q0" }
from genlayer import *

class NewsSentimentOracle(gl.Contract):
    topic: str
    sentiment: str
    confidence: str
    headline: str

    def __init__(self):
        self.topic = ""
        self.sentiment = "unknown"
        self.confidence = ""
        self.headline = ""

    @gl.public.write
    def analyze_sentiment(self, topic: str) -> None:
        def fetch():
            url = "https://news.google.com/search?q=" + topic + "&hl=en"
            return gl.get_webpage(url, mode="text")

        result = gl.eq_principles.eq_principle_prompt_non_comparative(
            fetch,
            task="Read latest news about " + topic + ". Is sentiment bullish, bearish, or neutral? Extract top headline. Respond: sentiment|confidence|headline",
            criteria="Format: sentiment|confidence|headline. Sentiment: bullish/bearish/neutral. Confidence: high/medium/low."
        )
        parts = str(result).strip().split("|")
        if len(parts) >= 3:
            self.sentiment = parts[0].strip()
            self.confidence = parts[1].strip()
            self.headline = parts[2].strip()
        self.topic = topic

    @gl.public.write
    def check_bullish(self, topic: str) -> None:
        def fetch():
            url = "https://news.google.com/search?q=" + topic + "&hl=en"
            return gl.get_webpage(url, mode="text")

        result = gl.eq_principles.eq_principle_prompt_non_comparative(
            fetch,
            task="Is the overall news sentiment about " + topic + " bullish? Respond only: true or false",
            criteria="Answer must be exactly: true or false"
        )
        self.topic = topic
        self.sentiment = str(result).strip()
        self.confidence = "high"
        self.headline = ""

    @gl.public.view
    def get_sentiment(self) -> str:
        return self.sentiment

    @gl.public.view
    def get_confidence(self) -> str:
        return self.confidence

    @gl.public.view
    def get_headline(self) -> str:
        return self.headline

-----

## Step 2: Deploy

Click Deploy — no parameters needed. Wait for Finalized status.

Save your Transaction Hash.

-----

## Step 3: Analyze News Sentiment

Call `analyze_sentiment` (Write method):
topic → "bitcoin"

Wait for Finalized (~30-60 seconds).

Then call `get_sentiment` (Read):
Result: "bullish" or "bearish" or "neutral"

Call `get_headline` (Read) to see the top news headline that influenced the verdict.

-----

## Step 4: Use the Binary Check

For contract logic that needs a simple true/false trigger, call `check_bullish`:
topic → "ethereum"

Then get_sentiment returns "true" or "false" — ready to use in conditional logic.

-----

## How It Works Under the Hood
1. You call analyze_sentiment("bitcoin")

2. Each GenLayer validator independently:
   → Fetches Google News for "bitcoin"
   → Sends content to their LLM
   → LLM evaluates sentiment

3. Validators compare results via Equivalence Principle
   → If majority agree → consensus reached
   → Result stored on-chain

4. You read get_sentiment() → "bullish"

No oracle. No trusted third party. Just AI validators reaching consensus.

-----

## Real-World Use Cases

DeFi Trading Trigger:
# Execute trade only if Bitcoin sentiment is bullish
if oracle.get_sentiment() == "bullish":
    execute_buy_order()

DAO Governance:
# Only pass proposal if community sentiment is positive
if oracle.get_sentiment() != "bearish":
    pass_proposal()

Risk Management:
# Pause protocol if negative news detected
if oracle.get_sentiment() == "bearish" and oracle.get_confidence() == "high":
    pause_protocol()

-----

## Tips

- Use `check_bullish` for contract logic — simpler and reaches consensus faster
- Use `analyze_sentiment` when you need the headline as evidence
- If validators disagree → retry, it usually resolves on 2nd attempt
- Try different topics: "ethereum", "GenLayer", "AI stocks", "Fed interest rates"

-----

*Built as part of the GenLayer Incentivized Builder Program.*
