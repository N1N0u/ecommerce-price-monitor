from sqlalchemy import select
from sqlalchemy.orm import Session

from database.models import Competitor


class CompetitorRepository:

    def __init__(self, db: Session):
        self.db = db

    # CREATE
    def create(self, name, website_url):

        competitor = Competitor(
            name=name,
            website_url=website_url
        )

        try:
            self.db.add(competitor)
            self.db.commit()
            self.db.refresh(competitor)

            return competitor

        except Exception:
            self.db.rollback()
            raise

    # READ BY ID
    def get_by_id(self, competitor_id):

        return self.db.get(Competitor, competitor_id)

    # READ BY WEBSITE
    def get_by_website(self, website_url):

        statement = select(Competitor).where(
            Competitor.website_url == website_url
        )

        return self.db.scalar(statement)

    # READ ALL
    def get_all(self):

        statement = select(Competitor).order_by(
            Competitor.id
        )

        return self.db.scalars(statement).all()

    # DELETE
    def delete(self, competitor_id):

        competitor = self.get_by_id(competitor_id)

        if competitor is None:
            return False

        try:
            self.db.delete(competitor)
            self.db.commit()

            return True

        except Exception:
            self.db.rollback()
            raise