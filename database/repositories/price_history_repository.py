from sqlalchemy import select, desc
from sqlalchemy.orm import Session

from database.models import PriceHistory


class PriceHistoryRepository:

    def __init__(self, db: Session):
        self.db = db

    # CREATE
    def create(
        self,
        listing_id,
        price,
        currency,
        availability,
        original_price=None
    ):

        history = PriceHistory(
            listing_id=listing_id,
            price=price,
            original_price=original_price,
            currency=currency,
            availability=availability
        )

        try:
            self.db.add(history)
            self.db.commit()
            self.db.refresh(history)

            return history

        except Exception:
            self.db.rollback()
            raise

    # READ BY ID
    def get_by_id(self, history_id):

        return self.db.get(PriceHistory, history_id)

    # GET ALL RECORDS FOR A LISTING
    def get_by_listing(self, listing_id):

        statement = (
            select(PriceHistory)
            .where(PriceHistory.listing_id == listing_id)
            .order_by(PriceHistory.scraped_at)
        )

        return self.db.scalars(statement).all()

    # GET LATEST PRICE
    def get_latest(self, listing_id):

        statement = (
            select(PriceHistory)
            .where(PriceHistory.listing_id == listing_id)
            .order_by(desc(PriceHistory.scraped_at))
            .limit(1)
        )

        return self.db.scalar(statement)

    # DELETE
    def delete(self, history_id):

        history = self.get_by_id(history_id)

        if history is None:
            return False

        try:
            self.db.delete(history)
            self.db.commit()

            return True

        except Exception:
            self.db.rollback()
            raise