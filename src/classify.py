from __future__ import annotations

from typing import Any


TOPIC_KEYWORDS = {
    "inflation": ["inflation", "cpi", "rate cut", "interest rate", "hotter-than-expected"],
    "oil": ["oil", "crude", "opec", "supply route", "energy"],
    "gold": ["gold", "safe haven", "defensive asset", "safety"],
    "earnings": ["earnings", "forecast", "revenue", "profit", "beat forecasts"],
    "geopolitics": ["war", "conflict", "geopolitical", "uncertainty", "middle east"],
    "supply_chain": ["shipping", "bottleneck", "supply chain", "logistics", "trade costs"],
}

TOPIC_TO_AFFECTED = {
    "inflation": ["Global Equities", "Growth Stocks", "Commodities"],
    "oil": ["Energy", "Commodities", "Global Equities"],
    "gold": ["Gold", "Defensive Assets", "Commodities"],
    "earnings": ["Technology", "Global Equities"],
    "geopolitics": ["Commodities", "Defensive Assets", "Global Equities"],
    "supply_chain": ["Industrials", "Consumer Goods", "Global Equities"],
    "other": ["Global Equities"],
}

TOPIC_TO_IMPACT = {
    "inflation": "High",
    "oil": "Medium",
    "gold": "Medium",
    "earnings": "Medium",
    "geopolitics": "High",
    "supply_chain": "Medium",
    "other": "Low",
}

WHY_IT_MATTERS = {
    "inflation": (
        "Higher inflation can affect interest-rate expectations and put pressure on equity valuations, "
        "especially in rate-sensitive areas of the market."
    ),
    "oil": (
        "Oil price changes can influence energy producers, transport costs, and broader inflation expectations."
    ),
    "gold": (
        "Gold often reacts to uncertainty and can reflect increased demand for defensive assets."
    ),
    "earnings": (
        "Strong or weak earnings can shift sentiment toward a sector and alter expectations for future growth."
    ),
    "geopolitics": (
        "Geopolitical risk can affect supply chains, commodity prices, and overall market sentiment."
    ),
    "supply_chain": (
        "Supply disruptions can raise costs for companies and affect margins across multiple sectors."
    ),
    "other": (
        "This story may affect market sentiment, but its direct impact is less clear from the available information."
    ),
}

CALM_TAKEAWAY = {
    "inflation": (
        "This matters broadly, but the strongest effects are usually concentrated in rate-sensitive parts of the market."
    ),
    "oil": (
        "This is most relevant for energy exposure and inflation-sensitive sectors, not every holding equally."
    ),
    "gold": (
        "This is more useful as a signal of caution than a reason to panic."
    ),
    "earnings": (
        "This may move one sector more than the market as a whole."
    ),
    "geopolitics": (
        "Monitor it closely, but diversified portfolios are not always affected equally or immediately."
    ),
    "supply_chain": (
        "This is worth watching if disruptions persist, but one headline alone may not change the bigger picture."
    ),
    "other": (
        "This may be worth noting, but there is not enough evidence here to treat it as a major portfolio event."
    ),
}


def normalize_text(article: dict[str, Any]) -> str:
    """Combine relevant article fields into a single lowercase text blob."""
    headline = article.get("headline", "")
    summary = article.get("summary", "")
    return f"{headline} {summary}".lower()


def detect_topic(article: dict[str, Any]) -> tuple[str, str]:
    """
    Returns:
      - topic
      - match_reason (for transparency)
    """
    text = normalize_text(article)

    topic_scores = {}
    match_reasons = {}

    for topic, keywords in TOPIC_KEYWORDS.items():
        score = 0
        matched = []

        for keyword in keywords:
            if keyword in text:
                score += 1
                matched.append(keyword)

        if score > 0:
            topic_scores[topic] = score
            match_reasons[topic] = matched

    if not topic_scores:
        return "other", "No keyword match"

    # pick topic with highest score
    best_topic = max(topic_scores, key=topic_scores.get)
    reason = f"Matched keywords: {', '.join(match_reasons[best_topic])}"

    return best_topic, reason


def get_affected_assets(topic: str) -> list[str]:
    """Return affected sectors/assets for a detected topic."""
    return TOPIC_TO_AFFECTED.get(topic, TOPIC_TO_AFFECTED["other"])


def get_impact_level(topic: str) -> str:
    """Return High / Medium / Low based on topic."""
    return TOPIC_TO_IMPACT.get(topic, TOPIC_TO_IMPACT["other"])


def get_why_it_matters(topic: str) -> str:
    """Return a short explanation template."""
    return WHY_IT_MATTERS.get(topic, WHY_IT_MATTERS["other"])


def get_calm_takeaway(topic: str) -> str:
    """Return a calm, anti-panic framing template."""
    return CALM_TAKEAWAY.get(topic, CALM_TAKEAWAY["other"])


def process_article(article: dict[str, Any]) -> dict[str, Any]:
    """Transform a raw article into your structured output format."""
    topic, match_reason = detect_topic(article)

    return {
        "headline": article.get("headline", ""),
        "topic": topic,
        "impact_level": get_impact_level(topic),
        "affected": get_affected_assets(topic),
        "why_it_matters": get_why_it_matters(topic),
        "calm_takeaway": get_calm_takeaway(topic),
        "source": article.get("source", ""),
        "match_reason": match_reason,
    }