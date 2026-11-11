from uuid import uuid4

from database.connection import SessionLocal
from database.repositories.product_repository import ProductRepository
from database.repositories.competitor_repository import CompetitorRepository
from database.repositories.listing_repository import ListingRepository


def main():

    db = SessionLocal()

    try:

        product_repo = ProductRepository(db)
        competitor_repo = CompetitorRepository(db)
        listing_repo = ListingRepository(db)

        # Create a test product
        product = product_repo.create(
            name="Test Gaming Mouse",
            category="Electronics",
            sku=f"MOUSE-{uuid4().hex[:8]}"
        )

        # Create two competitors
        competitor_a = competitor_repo.create(
            name="Test Store A",
            website_url=f"https://store-a-{uuid4().hex[:8]}.example.com"
        )

        competitor_b = competitor_repo.create(
            name="Test Store B",
            website_url=f"https://store-b-{uuid4().hex[:8]}.example.com"
        )

        # Create two listings for the same product
        listing_a = listing_repo.create(
            product_id=product.id,
            competitor_id=competitor_a.id,
            product_url="https://store-a.example.com/mouse"
        )

        listing_b = listing_repo.create(
            product_id=product.id,
            competitor_id=competitor_b.id,
            product_url="https://store-b.example.com/mouse"
        )

        print("\nListings created:")
        print(listing_a.id, listing_a.product_url)
        print(listing_b.id, listing_b.product_url)

        # Retrieve listings by product
        product_listings = listing_repo.get_by_product(product.id)

        print("\nListings for product:")

        for listing in product_listings:
            print(listing.id, listing.product_id, listing.competitor_id)

        # Retrieve listings by competitor
        competitor_listings = listing_repo.get_by_competitor(
            competitor_a.id
        )

        print("\nListings for competitor A:")

        for listing in competitor_listings:
            print(listing.id, listing.product_url)

        # Cleanup test records
        listing_repo.delete(listing_a.id)
        listing_repo.delete(listing_b.id)

        product_repo.delete(product.id)
        competitor_repo.delete(competitor_a.id)
        competitor_repo.delete(competitor_b.id)

        print("\nTest records cleaned successfully!")

    finally:
        db.close()


if __name__ == "__main__":
    main()