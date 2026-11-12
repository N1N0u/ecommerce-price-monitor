from database.connection import SessionLocal

from database.models import (
    Product,
    Competitor,
    ProductListing
)

from services.price_monitor_service import PriceMonitorService


def main():

    db = SessionLocal()

    try:

        # Create test product
        product = Product(
            name="Test Gaming Mouse",
            category="Electronics",
            sku="MONITOR-TEST-001"
        )

        competitor = Competitor(
            name="Monitoring Test Store",
            website_url="https://monitor-test.example.com"
        )

        db.add_all([product, competitor])
        db.flush()

        # Create product listing
        listing = ProductListing(
            product_id=product.id,
            competitor_id=competitor.id,
            product_url="https://monitor-test.example.com/mouse"
        )

        db.add(listing)
        db.commit()

        service = PriceMonitorService(db)

        print("\n--- FIRST OBSERVATION ---")

        result = service.record_observation(
            listing_id=listing.id,
            price=999.99,
            currency="GBP",
            availability="In stock"
        )

        print("Price recorded:", result["history"].price)
        print("Alerts generated:", len(result["alerts"]))

        print("\n--- SECOND OBSERVATION ---")

        result = service.record_observation(
            listing_id=listing.id,
            price=899.99,
            currency="GBP",
            availability="In stock"
        )

        print("Price recorded:", result["history"].price)

        for alert in result["alerts"]:
            print("Alert:", alert.alert_type)
            print("Message:", alert.message)

        print("\n--- THIRD OBSERVATION ---")

        result = service.record_observation(
            listing_id=listing.id,
            price=899.99,
            currency="GBP",
            availability="Out of stock"
        )

        print("Price recorded:", result["history"].price)

        for alert in result["alerts"]:
            print("Alert:", alert.alert_type)
            print("Message:", alert.message)

        # Cleanup test records
        db.delete(listing)
        db.delete(product)
        db.delete(competitor)

        db.commit()

        print("\nTest records cleaned successfully!")

    except Exception:

        db.rollback()
        raise

    finally:

        db.close()


if __name__ == "__main__":
    main()
