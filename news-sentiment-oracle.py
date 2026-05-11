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
