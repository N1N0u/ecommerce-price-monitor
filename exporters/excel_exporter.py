from pathlib import Path

import pandas as pd

from exporters.csv_exporter import CSVExporter


class ExcelExporter:

    def __init__(self, db):

        self.csv_exporter = CSVExporter(db)

        self.export_dir = Path("data/exports")

        self.export_dir.mkdir(
            parents=True,
            exist_ok=True
        )

    def export_all(self):

        # Generate CSV reports first
        latest_prices = self.csv_exporter.export_latest_prices()

        price_history = self.csv_exporter.export_price_history()

        alerts = self.csv_exporter.export_alerts()

        # Create Excel workbook
        file_path = self.export_dir / "price_monitor_report.xlsx"

        with pd.ExcelWriter(
            file_path,
            engine="openpyxl"
        ) as writer:

            pd.read_csv(latest_prices).to_excel(
                writer,
                sheet_name="Latest Prices",
                index=False
            )

            pd.read_csv(price_history).to_excel(
                writer,
                sheet_name="Price History",
                index=False
            )

            pd.read_csv(alerts).to_excel(
                writer,
                sheet_name="Alerts",
                index=False
            )

        return file_path