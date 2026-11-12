from database.models import ScraperConfig


class ScraperConfigRepository:

    def __init__(self, db):
        self.db = db

    def create(self, competitor_id, config):

        try:

            scraper_config = ScraperConfig(
                competitor_id=competitor_id,
                product_container=config["product_container"],
                name_selector=config["name_selector"],
                name_attribute=config.get("name_attribute"),
                price_selector=config["price_selector"],
                availability_selector=config.get("availability_selector"),
                product_url_selector=config["product_url_selector"],
                next_page_selector=config.get("next_page_selector"),
                currency=config["currency"],
                timeout=config.get("timeout", 30),
                enabled=config.get("enabled", True)
            )

            self.db.add(scraper_config)
            self.db.commit()
            self.db.refresh(scraper_config)

            return scraper_config

        except Exception:
            self.db.rollback()
            raise

    def get_by_id(self, config_id):

        return self.db.query(ScraperConfig).filter_by(
            id=config_id
        ).first()

    def get_by_competitor(self, competitor_id):

        return self.db.query(ScraperConfig).filter_by(
            competitor_id=competitor_id
        ).first()

    def get_all(self):

        return self.db.query(ScraperConfig).order_by(
            ScraperConfig.id
        ).all()

    def get_enabled(self):

        return self.db.query(ScraperConfig).filter_by(
            enabled=True
        ).all()

    def update(self, config_id, updates):

        scraper_config = self.get_by_id(config_id)

        if scraper_config is None:
            return None

        allowed_fields = {
            "product_container",
            "name_selector",
            "name_attribute",
            "price_selector",
            "availability_selector",
            "product_url_selector",
            "next_page_selector",
            "currency",
            "timeout",
            "enabled"
        }

        try:

            for field, value in updates.items():

                if field in allowed_fields:
                    setattr(scraper_config, field, value)

            self.db.commit()
            self.db.refresh(scraper_config)

            return scraper_config

        except Exception:
            self.db.rollback()
            raise

    def delete(self, config_id):

        scraper_config = self.get_by_id(config_id)

        if scraper_config is None:
            return False

        try:
            self.db.delete(scraper_config)
            self.db.commit()
            return True

        except Exception:
            self.db.rollback()
            raise
