# 📰 Build a News Sentiment Oracle on GenLayer — Tutorial

What we're building: An Intelligent Contract that fetches live news, analyzes sentiment, and stores the result on-chain — all without a centralized oracle.

Why this is powerful: Traditional smart contracts cannot read news. GenLayer contracts can — and multiple AI validators independently verify the sentiment before reaching consensus.

-----

## Prerequisites

- GenLayer Studio account at [studio.genlayer.com](https://studio.genlayer.com)
- Connected to Testnet Bradbury
- Test GEN tokens (use the Faucet)

-----

## Step 1: Create the Contract

Open Studio → click "+" → name it news_sentiment_oracle.py

Paste this code:

```python
# v0.1.0
# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }
from genlayer import *
import json


class NewsSentimentOracle(gl.Contract):
    """
    News Sentiment Oracle — Intelligent Contract

    Fetches live news about any topic and analyzes sentiment on-chain.
    AI validators independently fetch and evaluate news, then reach
    consensus on whether the sentiment is bullish, bearish, or neutral.

    Real-world use cases:
    - Trigger DeFi trades based on news sentiment
    - DAO governance — only execute proposal if community sentiment is positive
    - Prediction markets — resolve based on news coverage
    - Risk management — pause protocol if negative news detected
    """
    topic: str
    sentiment: str
    confidence: str
    headline: str
    last_updated: str

    def __init__(self):
        self.topic = ""
        self.sentiment = "unknown"
        self.confidence = ""
        self.headline = ""
        self.last_updated = ""

    @gl.public.write
    def analyze_sentiment(self, topic: str) -> None:
        """
        Fetch latest news about a topic and analyze sentiment.

        Args:
            topic: Any topic e.g. "bitcoin", "ethereum", "GenLayer", "Apple stock"
        """
        def fetch():
            url = "https://news.google.com/search?q=" + topic + "&hl=en"
            return gl.nondet.web.render(url, mode="text")

        result = gl.eq_principle.prompt_non_comparative(
            fetch,
            task="Read the latest news headlines about " + topic + ". Analyze the overall sentiment. Is the news mostly positive/bullish, negative/bearish, or neutral? Also extract the single most important headline. Respond with: sentiment|confidence|headline. Example: bullish|high|Bitcoin hits new all-time high as institutional demand surges",
            criteria="Answer must follow format: sentiment|confidence|headline where sentiment is bullish, bearish, or neutral, and confidence is high, medium, or low."
        )

        parts = str(result).strip().split("|")
        if len(parts) >= 3:
            self.sentiment = parts[0].strip().lower()
            self.confidence = parts[1].strip().lower()
            self.headline = parts[2].strip()
        else:
            self.sentiment = str(result).strip()
            self.confidence = "low"
            self.headline = "unable to extract"

        self.topic = topic
        self.last_updated = "latest"

    @gl.public.write
    def check_bullish(self, topic: str) -> None:
        """
        Simple bullish check — useful for triggering contract logic.
        Sets sentiment to 'true' if bullish, 'false' otherwise.

        Args:
            topic: Topic to check e.g. "bitcoin", "ethereum"
        """
        def fetch():
            url = "https://news.google.com/search?q=" + topic + "&hl=en"
            return gl.nondet.web.render(url, mode="text")

        result = gl.eq_principle.prompt_non_comparative(
            fetch,
            task="Based on the latest news headlines about " + topic + ", is the overall sentiment bullish/positive? Respond only: true or false",
            criteria="Answer must be exactly: true or false"
        )
        self.topic = topic
        self.sentiment = str(result).strip().lower()
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

    @gl.public.view
    def get_topic(self) -> str:
        return self.topic
```


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
   → Fetches Google News for "bitcoin" via `gl.nondet.web.render`
   → Sends content to their LLM
   → LLM evaluates sentiment

3. Validators compare results via Equivalence Principle (`gl.eq_principle.prompt_non_comparative`)
   → If majority agree → consensus reached
   → Result stored on-chain

4. You read get_sentiment() → "bullish"

No oracle. No trusted third party. Just AI validators reaching consensus.

-----

## Real-World Use Cases

### DeFi Trading Trigger:
```python
# Execute trade only if Bitcoin sentiment is bullish
if oracle.get_sentiment() == "bullish":
    execute_buy_order()
```

### DAO Governance:
```python
# Only pass proposal if community sentiment is positive
if oracle.get_sentiment() != "bearish":
    pass_proposal()
```

### Risk Management:
```python
# Pause protocol if negative news detected
if oracle.get_sentiment() == "bearish" and oracle.get_confidence() == "high":
    pause_protocol()
```

-----

## Tips

- Use `check_bullish` for contract logic — simpler and reaches consensus faster
- Use `analyze_sentiment` when you need the headline as evidence
- If validators disagree → retry, it usually resolves on 2nd attempt
- Try different topics: "ethereum", "GenLayer", "AI stocks", "Fed interest rates"

-----

*Built as part of the GenLayer Incentivized Builder Program.*
