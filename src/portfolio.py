from __future__ import annotations

from typing import Any


TICKER_TO_EXPOSURE = {
    "AAPL": ["Technology", "Global Equities"],
    "MSFT": ["Technology", "Global Equities"],
    "NVDA": ["Technology", "Global Equities"],
    "GOOGL": ["Technology", "Global Equities"],
    "XOM": ["Energy", "Global Equities"],
    "CVX": ["Energy", "Global Equities"],
    "GLD": ["Gold", "Commodities"],
    "USO": ["Oil", "Commodities"],
    "VT": ["Global Equities"],
    "VEA": ["Global Equities"],
    "VWO": ["Global Equities"],
}


def get_portfolio_exposures(portfolio: list[str]) -> dict[str, list[str]]:
    """
    Map each ticker in the portfolio to its known exposures.
    Unknown tickers get an empty list for now.
    """
    exposures: dict[str, list[str]] = {}

    for ticker in portfolio:
        exposures[ticker] = TICKER_TO_EXPOSURE.get(ticker.upper(), [])

    return exposures


def score_portfolio_relevance(
    processed_article: dict[str, Any],
    portfolio: list[str],
) -> dict[str, Any]:
    """
    Compare article affected assets/sectors against user portfolio exposures.
    Adds:
      - portfolio_relevance
      - relevant_holdings
      - overlap_tags
    """
    article_affected = set(processed_article.get("affected", []))
    portfolio_exposures = get_portfolio_exposures(portfolio)

    relevant_holdings: list[str] = []
    overlap_tags: set[str] = set()

    for ticker, exposures in portfolio_exposures.items():
        overlap = article_affected.intersection(exposures)
        if overlap:
            relevant_holdings.append(ticker)
            overlap_tags.update(overlap)

    overlap_count = len(overlap_tags)

    if overlap_count >= 2:
        relevance = "High"
    elif overlap_count == 1:
        relevance = "Medium"
    else:
        relevance = "Low"

    enriched_article = processed_article.copy()
    enriched_article["portfolio_relevance"] = relevance
    enriched_article["relevant_holdings"] = relevant_holdings
    enriched_article["overlap_tags"] = sorted(overlap_tags)

    return enriched_article