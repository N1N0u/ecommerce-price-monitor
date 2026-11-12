import logging

from sqlalchemy import select
from sqlalchemy.orm import Session

from database.models import (
    Product,
    Competitor,
    ProductListing
)

from scrapers.scraper_registry import ScraperRegistry
from scrapers.books_to_scrape import BooksToScrape

from services.price_monitor_service import PriceMonitorService


logger = logging.getLogger(__name__)


class ScrapingPipelineService:

    def __init__(self, db: Session):

        self.db = db
        self.registry = ScraperRegistry()
        self.price_monitor = PriceMonitorService(db)

    # --------------------------------------------------
    # COMPETITOR MANAGEMENT
    # --------------------------------------------------

    def get_or_create_competitor(self):

        website_url = BooksToScrape.BASE_URL.rstrip("/")

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

            logger.info(
                "Competitor created: %s",
                website_url
            )

        return competitor

    # --------------------------------------------------
    # PRODUCT AND LISTING MANAGEMENT
    # --------------------------------------------------

    def get_or_create_listing(self, competitor, scraped_product):

        product_url = scraped_product["product_url"]

        statement = select(ProductListing).where(
            ProductListing.competitor_id == competitor.id,
            ProductListing.product_url == product_url
        )

        listing = self.db.scalar(statement)

        if listing is not None:
            return listing

        # Find the product in our catalog
        statement = select(Product).where(
            Product.name == scraped_product["name"]
        )

        product = self.db.scalar(statement)

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

        # Create competitor listing
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

    # --------------------------------------------------
    # SCRAPING ONE COMPETITOR
    # --------------------------------------------------

    def scrape_and_save(self, page_url=None, competitor=None):

        results = {
            "competitor": None,
            "scraped": 0,
            "processed": 0,
            "failed": 0,
            "alerts": 0,
            "products": [],
            "errors": []
        }

        try:

            # If no competitor was supplied,
            # use Books to Scrape for backward compatibility.
            if competitor is None:
                competitor = self.get_or_create_competitor()

            results["competitor"] = competitor.name

            # Select the correct scraper
            scraper = self.registry.get_scraper(
                competitor.website_url
            )

            if scraper is None:

                raise ValueError(
                    f"No scraper registered for "
                    f"{competitor.website_url}"
                )

            # Determine starting URL
            if page_url is None:

                if isinstance(scraper, BooksToScrape):

                    page_url = (
                        scraper.BASE_URL + "catalogue/page-1.html"
                    )

                else:

                    page_url = competitor.website_url

            logger.info(
                "Starting scraping: %s",
                competitor.website_url
            )

            # Scrape all pages
            scraped_products = scraper.scrape_all_pages(
                page_url
            )

            results["scraped"] = len(scraped_products)

            # Ensure competitor exists before processing products
            self.db.commit()

            # Process each product individually
            for scraped_product in scraped_products:

                try:

                    listing = self.get_or_create_listing(
                        competitor,
                        scraped_product
                    )

                    observation = self.price_monitor.record_observation(
                        listing_id=listing.id,
                        price=scraped_product["price"],
                        currency=scraped_product["currency"],
                        availability=scraped_product["availability"]
                    )

                    results["processed"] += 1

                    results["alerts"] += len(
                        observation["alerts"]
                    )

                    results["products"].append({
                        "name": scraped_product["name"],
                        "price": scraped_product["price"],
                        "alerts": [
                            alert.alert_type
                            for alert in observation["alerts"]
                        ]
                    })

                except Exception as error:

                    self.db.rollback()

                    results["failed"] += 1

                    error_message = {
                        "product": scraped_product.get(
                            "name",
                            "Unknown product"
                        ),
                        "error": str(error)
                    }

                    results["errors"].append(error_message)

                    logger.exception(
                        "Failed to process product: %s",
                        error_message["product"]
                    )

            logger.info(
                "Competitor %s finished: %s processed, "
                "%s failed, %s alerts",
                competitor.name,
                results["processed"],
                results["failed"],
                results["alerts"]
            )

            return results

        except Exception as error:

            self.db.rollback()

            logger.exception(
                "Scraping failed for competitor: %s",
                results["competitor"]
            )

            results["errors"].append({
                "competitor": results["competitor"],
                "error": str(error)
            })

            results["failed"] += 1

            return results

    # --------------------------------------------------
    # SCRAPE ALL REGISTERED COMPETITORS
    # --------------------------------------------------

    def scrape_all_competitors(self):

        summary = {
            "competitors": 0,
            "supported": 0,
            "unsupported": 0,
            "scraped": 0,
            "processed": 0,
            "failed": 0,
            "alerts": 0,
            "results": [],
            "unsupported_websites": []
        }

        statement = select(Competitor).order_by(
            Competitor.id
        )

        competitors = self.db.scalars(statement).all()

        summary["competitors"] = len(competitors)

        for competitor in competitors:

            scraper = self.registry.get_scraper(
                competitor.website_url
            )

            if scraper is None:

                summary["unsupported"] += 1

                summary["unsupported_websites"].append(
                    competitor.website_url
                )

                logger.warning(
                    "No scraper available for %s",
                    competitor.website_url
                )

                continue

            summary["supported"] += 1

            result = self.scrape_and_save(
                competitor=competitor
            )

            summary["scraped"] += result["scraped"]
            summary["processed"] += result["processed"]
            summary["failed"] += result["failed"]
            summary["alerts"] += result["alerts"]

            summary["results"].append(result)

        logger.info(
            "All competitors finished: %s supported, "
            "%s unsupported, %s products processed",
            summary["supported"],
            summary["unsupported"],
            summary["processed"]
        )

        return summary