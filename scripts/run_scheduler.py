from config.logging_config import setup_logging

from scheduler.scraping_scheduler import ScrapingScheduler


def main():

    setup_logging()

    scheduler = ScrapingScheduler()

    print("\nStarting Ecommerce Price Monitoring Scheduler...")

    print("Press CTRL+C to stop.")

    scheduler.start()


if __name__ == "__main__":
    main()