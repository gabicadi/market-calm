from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from classify import process_article
from portfolio import score_portfolio_relevance


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "sample_news.json"
OUTPUT_PATH = BASE_DIR / "outputs" / "daily_summary.json"


def load_news(file_path: Path) -> list[dict[str, Any]]:
    """Load raw sample news from JSON."""
    with file_path.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_output(data: list[dict[str, Any]], file_path: Path) -> None:
    """Save processed output as pretty JSON."""
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with file_path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def main() -> None:
    """Run the full prototype pipeline."""
    raw_news = load_news(DATA_PATH)

    # Example portfolio for testing
    portfolio = ["AAPL", "MSFT", "GLD"]

    processed_news: list[dict[str, Any]] = []

    for article in raw_news:
        structured_article = process_article(article)
        enriched_article = score_portfolio_relevance(structured_article, portfolio)
        processed_news.append(enriched_article)

    save_output(processed_news, OUTPUT_PATH)

    print(f"Processed {len(processed_news)} articles.")
    print(f"Saved output to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()