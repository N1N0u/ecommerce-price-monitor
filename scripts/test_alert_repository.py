from uuid import uuid4

from database.connection import SessionLocal

from database.repositories.product_repository import ProductRepository
from database.repositories.competitor_repository import CompetitorRepository
from database.repositories.listing_repository import ListingRepository
from database.repositories.alert_repository import AlertRepository


def main():

    db = SessionLocal()

    try:

        product_repo = ProductRepository(db)
        competitor_repo = CompetitorRepository(db)
        listing_repo = ListingRepository(db)
        alert_repo = AlertRepository(db)

        # Create test product
        product = product_repo.create(
            name="Test Laptop",
            category="Electronics",
            sku=f"ALERT-{uuid4().hex[:8]}"
        )

        # Create competitor
        competitor = competitor_repo.create(
            name="Test Store",
            website_url=f"https://alert-{uuid4().hex[:8]}.example.com"
        )

        # Create listing
        listing = listing_repo.create(
            product_id=product.id,
            competitor_id=competitor.id,
            product_url="https://example.com/test-laptop"
        )

        # Create alert
        alert = alert_repo.create(
            listing_id=listing.id,
            alert_type="price_drop",
            old_value="999.99",
            new_value="899.99",
            message="Laptop price decreased from 999.99 to 899.99 GBP"
        )

        print("\nAlert created:")
        print(alert.id, alert.alert_type, alert.message)

        # Retrieve alert
        found = alert_repo.get_by_id(alert.id)

        print("\nAlert retrieved:")
        print(found.message)

        # Get unread alerts
        unread = alert_repo.get_unread()

        print("\nUnread alerts:", len(unread))

        # Mark as read
        alert_repo.mark_as_read(alert.id)

        updated_alert = alert_repo.get_by_id(alert.id)

        print("\nAlert read status:", updated_alert.is_read)

        # Cleanup
        alert_repo.delete(alert.id)
        listing_repo.delete(listing.id)
        product_repo.delete(product.id)
        competitor_repo.delete(competitor.id)

        print("\nTest records cleaned successfully!")

    finally:
        db.close()


if __name__ == "__main__":
    main()