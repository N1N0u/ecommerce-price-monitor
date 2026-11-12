import streamlit as st

import pandas as pd

import plotly.express as px

from sqlalchemy import select, func, desc

from database.connection import SessionLocal

from database.models import (
    Product,
    Competitor,
    ProductListing,
    PriceHistory,
    Alert
)


def show():

    st.header("Dashboard Overview")

    db = SessionLocal()

    try:

        # Total products
        total_products = db.scalar(
            select(func.count(Product.id))
        ) or 0

        # Total competitors
        total_competitors = db.scalar(
            select(func.count(Competitor.id))
        ) or 0

        # Total listings
        total_listings = db.scalar(
            select(func.count(ProductListing.id))
        ) or 0

        # Total alerts
        total_alerts = db.scalar(
            select(func.count(Alert.id))
        ) or 0

        # Display metrics
        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Products", total_products)

        col2.metric("Competitors", total_competitors)

        col3.metric("Listings", total_listings)

        col4.metric("Alerts", total_alerts)

        st.divider()

        st.subheader("Recent Price Observations")

        statement = (
            select(
                Product.name.label("product"),
                Competitor.name.label("competitor"),
                PriceHistory.price,
                PriceHistory.currency,
                PriceHistory.availability,
                PriceHistory.scraped_at
            )
            .join(
                ProductListing,
                Product.id == ProductListing.product_id
            )
            .join(
                Competitor,
                Competitor.id == ProductListing.competitor_id
            )
            .join(
                PriceHistory,
                PriceHistory.listing_id == ProductListing.id
            )
            .order_by(desc(PriceHistory.scraped_at))
            .limit(20)
        )

        rows = db.execute(statement).mappings().all()

        dataframe = pd.DataFrame(rows)

        if not dataframe.empty:

            st.dataframe(
                dataframe,
                use_container_width=True,
                hide_index=True
            )

            st.subheader("Latest Price Distribution")

            chart = px.histogram(
                dataframe,
                x="price",
                color="competitor",
                title="Price Distribution"
            )

            st.plotly_chart(
                chart,
                use_container_width=True
            )

        else:

            st.info("No price observations available yet.")

    finally:

        db.close()