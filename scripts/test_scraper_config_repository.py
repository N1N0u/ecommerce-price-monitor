from database.connection import SessionLocal
from database.models import Competitor
from database.repositories.scraper_config_repository import (
    ScraperConfigRepository
)

from config.scrapers.books_config import BOOKS_CONFIG


def main():

    db = SessionLocal()

    try:

        repository = ScraperConfigRepository(db)

        competitor = db.query(Competitor).filter_by(
            website_url="https://books.toscrape.com"
        ).first()

        if competitor is None:
            print("Competitor not found.")
            return

        existing = repository.get_by_competitor(
            competitor.id
        )

        if existing:
            print("Configuration already exists.")
            return

        config = repository.create(
            competitor_id=competitor.id,
            config=BOOKS_CONFIG
        )

        print("\nConfiguration created successfully!")

        print("ID:", config.id)
        print("Competitor ID:", config.competitor_id)
        print("Product container:", config.product_container)
        print("Name selector:", config.name_selector)
        print("Name attribute:", config.name_attribute)
        print("Price selector:", config.price_selector)
        print("Currency:", config.currency)
        print("Enabled:", config.enabled)

    finally:
        db.close()


if __name__ == "__main__":
    main()