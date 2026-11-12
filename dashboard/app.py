import sys
from pathlib import Path

import streamlit as st

# Add the project root to Python's import path
PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Import dashboard pages
from dashboard.pages import (
    overview,
    competitors,
    price_history,
    alerts,
    exports
)


st.set_page_config(
    page_title="Ecommerce Price Monitor",
    page_icon="📊",
    layout="wide"
)

st.title("E-commerce Price Monitoring System")

st.caption(
    "Monitor competitor prices, track historical changes "
    "and detect market opportunities."
)

page = st.sidebar.radio(
    "Navigation",
    [
        "Overview",
        "Competitors",
        "Price History",
        "Alerts",
        "Exports"
    ]
)

if page == "Overview":
    overview.show()

elif page == "Competitors":
    competitors.show()

elif page == "Price History":
    price_history.show()

elif page == "Alerts":
    alerts.show()

elif page == "Exports":
    exports.show()