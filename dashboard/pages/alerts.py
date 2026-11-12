import streamlit as st

import pandas as pd

from sqlalchemy import select, desc

from database.connection import SessionLocal

from database.models import (
    Alert,
    ProductListing,
    Product,
    Competitor
)


def show():

    st.header("Price Monitoring Alerts")

    db = SessionLocal()

    try:

        statement = (
            select(
                Product.name.label("product"),
                Competitor.name.label("competitor"),
                Alert.alert_type,
                Alert.old_value,
                Alert.new_value,
                Alert.message,
                Alert.created_at,
                Alert.is_read
            )
            .join(
                ProductListing,
                Alert.listing_id == ProductListing.id
            )
            .join(
                Product,
                ProductListing.product_id == Product.id
            )
            .join(
                Competitor,
                ProductListing.competitor_id == Competitor.id
            )
            .order_by(desc(Alert.created_at))
        )

        rows = db.execute(statement).mappings().all()

        dataframe = pd.DataFrame(rows)

        if dataframe.empty:

            st.success("No alerts available.")

        else:

            unread = dataframe[
                dataframe["is_read"] == False
            ]

            st.metric(
                "Unread alerts",
                len(unread)
            )

            st.dataframe(
                dataframe,
                use_container_width=True,
                hide_index=True
            )

    finally:

        db.close()