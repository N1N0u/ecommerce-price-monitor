import logging

from datetime import datetime

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger

from database.connection import SessionLocal

from services.scraping_pipeline_service import (
    ScrapingPipelineService
)

from config.settings import SCRAPE_INTERVAL_HOURS


logger = logging.getLogger(__name__)


class ScrapingScheduler:

    def __init__(self):

        self.scheduler = BlockingScheduler()

    def run_scraping_job(self):

        logger.info("Starting scheduled scraping job")

        db = SessionLocal()

        try:

            pipeline = ScrapingPipelineService(db)

            page_url = (
                "https://books.toscrape.com/catalogue/page-1.html"
            )

            results = pipeline.scrape_and_save(page_url)

            logger.info(
                "Scheduled scraping completed: "
                "%s scraped, %s processed, %s failed, %s alerts",
                results["scraped"],
                results["processed"],
                results["failed"],
                results["alerts"]
            )

        except Exception:

            logger.exception("Scheduled scraping failed")

        finally:

            db.close()

    def start(self):

        logger.info(
            "Starting scheduler. Interval: %s hours",
            SCRAPE_INTERVAL_HOURS
        )

        self.scheduler.add_job(
            self.run_scraping_job,
            trigger=IntervalTrigger(
                hours=SCRAPE_INTERVAL_HOURS
            ),
            id="competitor_price_monitor",
            name="Competitor Price Monitoring",
            max_instances=1,
            coalesce=True,
            misfire_grace_time=3600,
            next_run_time=datetime.now()
        )

        try:

            self.scheduler.start()

        except (KeyboardInterrupt, SystemExit):

            logger.info("Stopping scheduler")

            self.scheduler.shutdown()