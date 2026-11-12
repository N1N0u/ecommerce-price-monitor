import csv
from pathlib import Path

from sqlalchemy import select, desc

from database.models import (
    Product,
    Competitor,
    ProductListing,
    PriceHistory,
    Alert
)


class CSVExporter:

    def __init__(self, db):

        self.db = db

        self.export_dir = Path("data/exports")

        self.export_dir.mkdir(
            parents=True,
            exist_ok=True
        )

    def export_latest_prices(self):

        statement = (
            select(
                Product.name,
                Competitor.name,
                ProductListing.product_url,
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
            .order_by(
                Product.name,
                Competitor.name,
                desc(PriceHistory.scraped_at),
                desc(PriceHistory.id)
            )
        )

        rows = self.db.execute(statement).all()

        # Keep only the latest observation per listing
        latest_rows = {}
        for row in rows:
            listing_key = row.product_url

            if listing_key not in latest_rows:
                latest_rows[listing_key] = row

        file_path = self.export_dir / "latest_prices.csv"

        headers = [
            "Product",
            "Competitor",
            "Product URL",
            "Price",
            "Currency",
            "Availability",
            "Scraped At"
        ]

        with open(
            file_path,
            "w",
            newline="",
            encoding="utf-8-sig"
        ) as file:

            writer = csv.writer(file)

            writer.writerow(headers)

            for row in latest_rows.values():

                writer.writerow(row)

        return file_path

    def export_price_history(self):

        statement = (
            select(
                Product.name,
                Competitor.name,
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
            .order_by(PriceHistory.scraped_at)
        )

        rows = self.db.execute(statement).all()

        file_path = self.export_dir / "price_history.csv"

        headers = [
            "Product",
            "Competitor",
            "Price",
            "Currency",
            "Availability",
            "Scraped At"
        ]

        with open(
            file_path,
            "w",
            newline="",
            encoding="utf-8-sig"
        ) as file:

            writer = csv.writer(file)

            writer.writerow(headers)

            writer.writerows(rows)

        return file_path

    def export_alerts(self):

        statement = (
            select(
                Product.name,
                Competitor.name,
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
                Product.id == ProductListing.product_id
            )
            .join(
                Competitor,
                Competitor.id == ProductListing.competitor_id
            )
            .order_by(desc(Alert.created_at))
        )

        rows = self.db.execute(statement).all()

        file_path = self.export_dir / "alerts.csv"

        headers = [
            "Product",
            "Competitor",
            "Alert Type",
            "Old Value",
            "New Value",
            "Message",
            "Created At",
            "Read"
        ]

        with open(
            file_path,
            "w",
            newline="",
            encoding="utf-8-sig"
        ) as file:

            writer = csv.writer(file)

            writer.writerow(headers)

            writer.writerows(rows)

        return file_path