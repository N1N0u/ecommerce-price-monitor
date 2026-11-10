from database.connection import SessionLocal
from database.models import Product, Competitor, ProductListing


def test_database():

    db = SessionLocal()

    try:

        product = Product(
            name="Wireless Bluetooth Headphones",
            category="Electronics",
            sku="HEADPHONES-001"
        )

        competitor = Competitor(
            name="Demo Store A",
            website_url="https://store-a.example.com"
        )

        db.add(product)
        db.add(competitor)

        db.flush()

        listing = ProductListing(
            product_id=product.id,
            competitor_id=competitor.id,
            product_url="https://store-a.example.com/headphones"
        )

        db.add(listing)

        db.commit()

        print("Product, competitor and listing inserted successfully!")

    except Exception:

        db.rollback()
        raise

    finally:

        db.close()


if __name__ == "__main__":
    test_database()
