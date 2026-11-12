from database.connection import SessionLocal

from exporters.csv_exporter import CSVExporter
from exporters.excel_exporter import ExcelExporter


def main():

    db = SessionLocal()

    try:

        print("\nStarting data exports...")

        # CSV exports
        csv_exporter = CSVExporter(db)

        latest_prices = csv_exporter.export_latest_prices()

        price_history = csv_exporter.export_price_history()

        alerts = csv_exporter.export_alerts()

        print("\nCSV EXPORTS")

        print("Latest prices:", latest_prices)

        print("Price history:", price_history)

        print("Alerts:", alerts)

        # Excel export
        excel_exporter = ExcelExporter(db)

        excel_file = excel_exporter.export_all()

        print("\nEXCEL EXPORT")

        print("Excel report:", excel_file)

        print("\nAll exports completed successfully!")

    finally:

        db.close()


if __name__ == "__main__":
    main()