import uuid

from database.connection import SessionLocal

from database.models import (
    Product,
    Competitor,
    ProductListing
)

from services.price_monitor_service import PriceMonitorService
from services.price_comparison_service import PriceComparisonService


def main():

    db = SessionLocal()

    test_id = uuid.uuid4().hex[:8]
    
    try:

        # Create test product
        product = Product(
            name="Wireless Gaming Mouse",
            category="Electronics",
            sku=f"COMPARISON-{test_id}"
        )

        # Create two competitors
        competitor_a = Competitor(
            name="Demo Store A",
            website_url=f"https://store-a-{test_id}.example.com"
        )

        competitor_b = Competitor(
            name="Demo Store B",
            website_url=f"https://store-b-{test_id}.example.com"
        )

        db.add_all([
            product,
            competitor_a,
            competitor_b
        ])

        db.flush()

        # Create competitor listings
        listing_a = ProductListing(
            product_id=product.id,
            competitor_id=competitor_a.id,
            product_url=(
                f"https://store-a-{test_id}.example.com/mouse"
            )
        )

        listing_b = ProductListing(
            product_id=product.id,
            competitor_id=competitor_b.id,
            product_url=(
                f"https://store-b-{test_id}.example.com/mouse"
            )
        )

        db.add_all([listing_a, listing_b])

        db.commit()

        # Record prices
        monitor = PriceMonitorService(db)

        monitor.record_observation(
            listing_id=listing_a.id,
            price=999.99,
            currency="GBP",
            availability="In stock"
        )

        monitor.record_observation(
            listing_id=listing_b.id,
            price=899.99,
            currency="GBP",
            availability="In stock"
        )

        # Compare prices
        comparison = PriceComparisonService(db)

        result = comparison.compare_product_prices(
            product.id
        )

        print("\nPRODUCT:", result["product"])

        print("\nPRICE COMPARISON")

        for offer in result["offers"]:

            print("-" * 40)

            print("Competitor:", offer["competitor"])

            print(
                "Price:",
                offer["price"],
                offer["currency"]
            )

            print("Availability:", offer["availability"])

        print("\nCHEAPEST OFFER")

        cheapest = result["cheapest_offer"]

        if cheapest:

            print("Competitor:", cheapest["competitor"])

            print(
                "Price:",
                cheapest["price"],
                cheapest["currency"]
            )

        print(
            "\nTotal competitors:",
            result["total_competitors"]
        )

        # Cleanup
        db.delete(product)
        db.delete(competitor_a)
        db.delete(competitor_b)

        db.commit()

        print("\nTest records cleaned successfully!")

    except Exception:

        db.rollback()
        raise

    finally:

        db.close()


if __name__ == "__main__":
    main()