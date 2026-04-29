import json
from pathlib import Path

import streamlit as st

from src.classify import process_article
from src.portfolio import score_portfolio_relevance


DATA_PATH = Path("data/sample_news.json")

st.set_page_config(
    page_title="Market Calm",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
        .main {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }

        .hero {
            padding: 1.2rem 1.4rem;
            border: 1px solid rgba(120, 120, 120, 0.2);
            border-radius: 16px;
            margin-bottom: 1.2rem;
            background-color: #fafafa;
        }

        .section-card {
            padding: 1rem 1.2rem;
            border: 1px solid rgba(120, 120, 120, 0.18);
            border-radius: 16px;
            background-color: white;
            margin-bottom: 1rem;
        }

        .story-card {
            padding: 1.1rem 1.2rem;
            border: 1px solid rgba(120, 120, 120, 0.18);
            border-radius: 16px;
            background-color: white;
            margin-bottom: 1rem;
        }

        .label {
            font-size: 0.82rem;
            color: #666;
            margin-bottom: 0.15rem;
        }

        .headline {
            font-size: 1.2rem;
            font-weight: 700;
            line-height: 1.35;
            margin-bottom: 0.7rem;
        }

        .summary-text {
            font-size: 1rem;
            line-height: 1.55;
            color: #222;
        }

        .pill {
            display: inline-block;
            padding: 0.28rem 0.65rem;
            border-radius: 999px;
            font-size: 0.78rem;
            font-weight: 600;
            margin-right: 0.45rem;
            margin-bottom: 0.4rem;
            border: 1px solid transparent;
        }

        .pill-neutral {
            background-color: #f3f4f6;
            color: #222;
            border-color: #e5e7eb;
        }

        .pill-high {
            background-color: #fee2e2;
            color: #991b1b;
            border-color: #fecaca;
        }

        .pill-medium {
            background-color: #fef3c7;
            color: #92400e;
            border-color: #fde68a;
        }

        .pill-low {
            background-color: #dcfce7;
            color: #166534;
            border-color: #bbf7d0;
        }

        .small-note {
            color: #666;
            font-size: 0.84rem;
            margin-top: 0.4rem;
        }

        .asset-tag {
            display: inline-block;
            padding: 0.22rem 0.55rem;
            border-radius: 999px;
            font-size: 0.77rem;
            background-color: #f5f5f5;
            color: #333;
            margin-right: 0.35rem;
            margin-bottom: 0.35rem;
            border: 1px solid #e8e8e8;
        }

        a {
            text-decoration: none !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


def load_raw_news() -> list[dict]:
    if not DATA_PATH.exists():
        st.error("Sample news file not found.")
        st.stop()

    with DATA_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def build_daily_summary(processed_news: list[dict]) -> str:
    high_impact_topics = sorted({a["topic"] for a in processed_news if a["impact_level"] == "High"})
    if high_impact_topics:
        pretty_topics = ", ".join(high_impact_topics)
        return f"Markets are mainly reacting to {pretty_topics} today. Focus on broad exposure first, not headline intensity."
    return "Markets are relatively stable today, with no clearly broad-impact event standing out above the rest."


def sort_articles(processed_news: list[dict]) -> list[dict]:
    relevance_order = {"High": 0, "Medium": 1, "Low": 2}
    impact_order = {"High": 0, "Medium": 1, "Low": 2}

    return sorted(
        processed_news,
        key=lambda x: (
            relevance_order.get(x.get("portfolio_relevance", "Low"), 3),
            impact_order.get(x.get("impact_level", "Low"), 3),
            x.get("headline", ""),
        ),
    )


def impact_pill(level: str) -> str:
    level = level.strip().lower()
    css_class = {
        "high": "pill-high",
        "medium": "pill-medium",
        "low": "pill-low",
    }.get(level, "pill-neutral")
    return f'<span class="pill {css_class}">Impact: {level.title()}</span>'


def relevance_pill(level: str) -> str:
    level = level.strip().lower()
    css_class = {
        "high": "pill-high",
        "medium": "pill-medium",
        "low": "pill-low",
    }.get(level, "pill-neutral")
    return f'<span class="pill {css_class}">Portfolio relevance: {level.title()}</span>'


def render_asset_tags(items: list[str]) -> str:
    return "".join([f'<span class="asset-tag">{item}</span>' for item in items])


st.title("Market Calm")
st.caption("A calm daily read on what matters for your portfolio.")

left, right = st.columns([2.2, 1.2], gap="large")

with left:
    st.markdown('<div class="hero">', unsafe_allow_html=True)
    st.subheader("Your Portfolio")
    portfolio_input = st.text_input(
        "Enter tickers separated by commas",
        value="AAPL, MSFT, GLD",
        label_visibility="collapsed",
        placeholder="AAPL, MSFT, GLD",
    )
    st.markdown(
        '<div class="small-note">Try examples like AAPL, MSFT, GLD or XOM, CVX or VT.</div>',
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

with right:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("### Design Goal")
    st.write("Reduce panic, surface relevance, and keep only essential information.")
    st.markdown("</div>", unsafe_allow_html=True)

portfolio = [ticker.strip().upper() for ticker in portfolio_input.split(",") if ticker.strip()]

raw_news = load_raw_news()

processed_news = []
for article in raw_news:
    structured_article = process_article(article)
    enriched_article = score_portfolio_relevance(structured_article, portfolio)
    processed_news.append(enriched_article)

processed_news = sort_articles(processed_news)
daily_summary = build_daily_summary(processed_news)

st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown("### Today's Read")
st.write(daily_summary)
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("### Top Stories")

for article in processed_news:
    st.markdown('<div class="story-card">', unsafe_allow_html=True)

    st.markdown(f'<div class="headline">{article["headline"]}</div>', unsafe_allow_html=True)

    pill_row = impact_pill(article["impact_level"]) + relevance_pill(article["portfolio_relevance"])
    st.markdown(pill_row, unsafe_allow_html=True)

    st.markdown('<div class="label">Affected sectors / assets</div>', unsafe_allow_html=True)
    st.markdown(render_asset_tags(article["affected"]), unsafe_allow_html=True)

    st.markdown('<div class="label">Why it matters</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="summary-text">{article["why_it_matters"]}</div>', unsafe_allow_html=True)

    st.markdown('<div class="label" style="margin-top: 0.8rem;">Calm takeaway</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="summary-text">{article["calm_takeaway"]}</div>', unsafe_allow_html=True)

    if article.get("relevant_holdings"):
        holdings = ", ".join(article["relevant_holdings"])
        st.markdown(
            f'<div class="small-note"><strong>Relevant holdings:</strong> {holdings}</div>',
            unsafe_allow_html=True,
        )

    if article.get("match_reason"):
        st.markdown(
            f'<div class="small-note"><strong>Classification reason:</strong> {article["match_reason"]}</div>',
            unsafe_allow_html=True,
        )

    st.markdown(f"[Open source article]({article['source']})")
    st.markdown("</div>", unsafe_allow_html=True)