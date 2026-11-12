import streamlit as st

import pandas as pd

import plotly.express as px

from sqlalchemy import select, desc

from database.connection import SessionLocal

from database.models import (
    Product,
    ProductListing,
    PriceHistory,
    Competitor
)


def show():

    st.header("Historical Price Tracking")

    db = SessionLocal()

    try:

        statement = (
            select(Product.id, Product.name)
            .order_by(Product.name)
        )

        products = db.execute(statement).all()

        if not products:

            st.info("No products available.")

            return

        product_options = {
            name: product_id
            for product_id, name in products
        }

        selected_name = st.selectbox(
            "Select a product",
            list(product_options.keys())
        )

        product_id = product_options[selected_name]

        history_statement = (
            select(
                PriceHistory.price,
                PriceHistory.currency,
                PriceHistory.scraped_at,
                Competitor.name.label("competitor")
            )
            .join(
                ProductListing,
                ProductListing.id == PriceHistory.listing_id
            )
            .join(
                Competitor,
                Competitor.id == ProductListing.competitor_id
            )
            .where(
                ProductListing.product_id == product_id
            )
            .order_by(PriceHistory.scraped_at)
        )

        rows = db.execute(
            history_statement
        ).mappings().all()

        dataframe = pd.DataFrame(rows)

        if not dataframe.empty:

            chart = px.line(
                dataframe,
                x="scraped_at",
                y="price",
                color="competitor",
                title=f"Price History: {selected_name}",
                markers=True
            )

            st.plotly_chart(
                chart,
                use_container_width=True
            )

            st.dataframe(
                dataframe,
                use_container_width=True,
                hide_index=True
            )

        else:

            st.info("No price history available.")

    finally:

        db.close()