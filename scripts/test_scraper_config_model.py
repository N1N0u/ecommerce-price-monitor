from database.connection import Base, engine, SessionLocal
from database.models import Competitor, ScraperConfig


def main():

    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:

        competitor = db.query(Competitor).filter_by(
            website_url="https://books.toscrape.com"
        ).first()

        if competitor is None:
            print("Competitor not found.")
            return

        print("Competitor:", competitor.name)

        print(
            "Scraper configuration:",
            competitor.scraper_config
        )

        print("ScraperConfig model imported successfully.")

    finally:
        db.close()


if __name__ == "__main__":
    main()