from uuid import uuid4

from database.connection import SessionLocal

from database.repositories.product_repository import ProductRepository
from database.repositories.competitor_repository import CompetitorRepository
from database.repositories.listing_repository import ListingRepository
from database.repositories.price_history_repository import PriceHistoryRepository


def main():

    db = SessionLocal()

    try:

        product_repo = ProductRepository(db)
        competitor_repo = CompetitorRepository(db)
        listing_repo = ListingRepository(db)
        history_repo = PriceHistoryRepository(db)

        # Create test product
        product = product_repo.create(
            name="Test Laptop",
            category="Electronics",
            sku=f"LAPTOP-{uuid4().hex[:8]}"
        )

        # Create test competitor
        competitor = competitor_repo.create(
            name="Test Laptop Store",
            website_url=f"https://laptop-{uuid4().hex[:8]}.example.com"
        )

        # Create listing
        listing = listing_repo.create(
            product_id=product.id,
            competitor_id=competitor.id,
            product_url="https://example.com/laptop"
        )

        # Record three price observations
        prices = [999.99, 949.99, 899.99]

        for price in prices:

            history = history_repo.create(
                listing_id=listing.id,
                price=price,
                original_price=1099.99,
                currency="GBP",
                availability="In stock"
            )

            print("Price recorded:", history.price)

        # Retrieve all history
        history_records = history_repo.get_by_listing(listing.id)

        print("\nPrice history:")

        for record in history_records:
            print(record.price, record.currency, record.availability)

        # Retrieve latest observation
        latest = history_repo.get_latest(listing.id)

        print("\nLatest price:", latest.price)

        # Cleanup
        for record in history_records:
            history_repo.delete(record.id)

        listing_repo.delete(listing.id)
        product_repo.delete(product.id)
        competitor_repo.delete(competitor.id)

        print("\nTest records cleaned successfully!")

    finally:
        db.close()


if __name__ == "__main__":
    main()