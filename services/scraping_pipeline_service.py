import logging

from sqlalchemy import select
from sqlalchemy.orm import Session

from database.models import (
    Product,
    Competitor,
    ProductListing
)

from scrapers.books_to_scrape import BooksToScrape
from services.price_monitor_service import PriceMonitorService


logger = logging.getLogger(__name__)


class ScrapingPipelineService:

    def __init__(self, db: Session):

        self.db = db
        self.scraper = BooksToScrape()
        self.price_monitor = PriceMonitorService(db)

    def get_or_create_competitor(self):

        website_url = self.scraper.BASE_URL.rstrip("/")

        statement = select(Competitor).where(
            Competitor.website_url == website_url
        )

        competitor = self.db.scalar(statement)

        if competitor is None:

            competitor = Competitor(
                name="Books To Scrape",
                website_url=website_url
            )

            self.db.add(competitor)
            self.db.flush()

            logger.info("Competitor created: %s", website_url)

        return competitor

    def get_or_create_listing(self, competitor, scraped_product):

        product_url = scraped_product["product_url"]

        # Check whether this listing already exists
        statement = select(ProductListing).where(
            ProductListing.competitor_id == competitor.id,
            ProductListing.product_url == product_url
        )

        listing = self.db.scalar(statement)

        if listing is not None:
            return listing

        # Try to find the same product in our catalog
        statement = select(Product).where(
            Product.name == scraped_product["name"]
        )

        product = self.db.scalar(statement)

        # Create the product if it doesn't exist
        if product is None:

            product = Product(
                name=scraped_product["name"]
            )

            self.db.add(product)
            self.db.flush()

            logger.info(
                "Product created: %s",
                product.name
            )

        # Create the competitor listing
        listing = ProductListing(
            product_id=product.id,
            competitor_id=competitor.id,
            product_url=product_url
        )

        self.db.add(listing)
        self.db.flush()

        logger.info(
            "Product listing created: %s",
            product_url
        )

        return listing

    def scrape_and_save(self, page_url):

        results = {
            "scraped": 0,
            "processed": 0,
            "alerts": 0,
            "products": []
        }

        try:

            # 1. Download and extract products
            scraped_products = self.scraper.scrape_page(
                page_url
            )

            results["scraped"] = len(scraped_products)

            # 2. Find or create competitor
            competitor = self.get_or_create_competitor()

            # 3. Process every scraped product
            for scraped_product in scraped_products:

                listing = self.get_or_create_listing(
                    competitor,
                    scraped_product
                )

                # 4. Record the price and detect changes
                observation = self.price_monitor.record_observation(
                    listing_id=listing.id,
                    price=scraped_product["price"],
                    currency=scraped_product["currency"],
                    availability=scraped_product["availability"]
                )

                results["processed"] += 1
                results["alerts"] += len(observation["alerts"])

                results["products"].append({
                    "name": scraped_product["name"],
                    "price": scraped_product["price"],
                    "alerts": [
                        alert.alert_type
                        for alert in observation["alerts"]
                    ]
                })

            logger.info(
                "Pipeline completed: %s products processed, %s alerts generated",
                results["processed"],
                results["alerts"]
            )

            return results

        except Exception:

            self.db.rollback()

            logger.exception("Scraping pipeline failed")

            raise