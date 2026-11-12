import streamlit as st

from database.connection import SessionLocal

from exporters.csv_exporter import CSVExporter

from exporters.excel_exporter import ExcelExporter


def show():

    st.header("Data Exports")

    db = SessionLocal()

    try:

        csv_exporter = CSVExporter(db)

        excel_exporter = ExcelExporter(db)

        st.subheader("CSV Reports")

        if st.button("Generate Latest Prices CSV"):

            path = csv_exporter.export_latest_prices()

            with open(path, "rb") as file:

                st.download_button(
                    "Download Latest Prices",
                    file,
                    file_name="latest_prices.csv"
                )

        if st.button("Generate Price History CSV"):

            path = csv_exporter.export_price_history()

            with open(path, "rb") as file:

                st.download_button(
                    "Download Price History",
                    file,
                    file_name="price_history.csv"
                )

        if st.button("Generate Alerts CSV"):

            path = csv_exporter.export_alerts()

            with open(path, "rb") as file:

                st.download_button(
                    "Download Alerts",
                    file,
                    file_name="alerts.csv"
                )

        st.divider()

        st.subheader("Excel Report")

        if st.button("Generate Excel Report"):

            path = excel_exporter.export_all()

            with open(path, "rb") as file:

                st.download_button(
                    "Download Excel Report",
                    file,
                    file_name="price_monitor_report.xlsx"
                )

    finally:

        db.close()