from sqlalchemy import select, desc
from sqlalchemy.orm import Session

from database.models import (
    Product,
    ProductListing,
    Competitor,
    PriceHistory
)


class PriceComparisonService:

    def __init__(self, db: Session):
        self.db = db

    def compare_product_prices(self, product_id):

        # 1. Check that the product exists
        product = self.db.get(Product, product_id)

        if product is None:
            raise ValueError(
                f"Product {product_id} does not exist."
            )

        # 2. Retrieve all competitor listings for this product
        statement = (
            select(ProductListing, Competitor)
            .join(
                Competitor,
                ProductListing.competitor_id == Competitor.id
            )
            .where(ProductListing.product_id == product_id)
        )

        listings = self.db.execute(statement).all()

        offers = []

        # 3. Find the latest price for each competitor
        for listing, competitor in listings:

            price_statement = (
                select(PriceHistory)
                .where(
                    PriceHistory.listing_id == listing.id
                )
                .order_by(
                    desc(PriceHistory.scraped_at),
                    desc(PriceHistory.id)
                )
                .limit(1)
            )

            latest_price = self.db.scalar(price_statement)

            # Skip listings without price history
            if latest_price is None:
                continue

            offer = {
                "competitor": competitor.name,
                "price": latest_price.price,
                "currency": latest_price.currency,
                "availability": latest_price.availability,
                "product_url": listing.product_url,
                "scraped_at": latest_price.scraped_at
            }

            offers.append(offer)

        # 4. Avoid comparing different currencies
        currencies = {
            offer["currency"]
            for offer in offers
        }

        if len(currencies) > 1:
            raise ValueError(
                "Cannot compare prices with different currencies."
            )

        # 5. Sort offers from cheapest to most expensive
        offers.sort(
            key=lambda offer: offer["price"]
        )

        # 6. Identify the cheapest offer
        cheapest_offer = offers[0] if offers else None

        return {
            "product": product.name,
            "offers": offers,
            "cheapest_offer": cheapest_offer,
            "total_competitors": len(offers)
        }