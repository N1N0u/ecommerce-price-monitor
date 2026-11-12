import streamlit as st

import pandas as pd

from sqlalchemy import select

from database.connection import SessionLocal

from database.models import (
    Product,
    Competitor,
    ProductListing,
    PriceHistory
)


def show():

    st.header("Competitor Price Comparison")

    db = SessionLocal()

    try:

        statement = (
            select(
                Product.name.label("product"),
                Competitor.name.label("competitor"),
                PriceHistory.price,
                PriceHistory.currency,
                PriceHistory.availability,
                ProductListing.product_url
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
            .order_by(Product.name, PriceHistory.price)
        )

        rows = db.execute(statement).mappings().all()

        dataframe = pd.DataFrame(rows)

        if dataframe.empty:

            st.info("No competitor data available.")

        else:

            products = sorted(
                dataframe["product"].unique()
            )

            selected_product = st.selectbox(
                "Select a product",
                products
            )

            filtered = dataframe[
                dataframe["product"] == selected_product
            ]

            st.dataframe(
                filtered,
                use_container_width=True,
                hide_index=True
            )

    finally:

        db.close()