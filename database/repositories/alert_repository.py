from sqlalchemy import select, desc
from sqlalchemy.orm import Session

from database.models import Alert


class AlertRepository:

    def __init__(self, db: Session):
        self.db = db

    # CREATE
    def create(
        self,
        listing_id,
        alert_type,
        message,
        old_value=None,
        new_value=None
    ):

        alert = Alert(
            listing_id=listing_id,
            alert_type=alert_type,
            message=message,
            old_value=old_value,
            new_value=new_value
        )

        try:
            self.db.add(alert)
            self.db.commit()
            self.db.refresh(alert)

            return alert

        except Exception:
            self.db.rollback()
            raise

    # READ BY ID
    def get_by_id(self, alert_id):

        return self.db.get(Alert, alert_id)

    # GET ALL ALERTS
    def get_all(self):

        statement = select(Alert).order_by(
            desc(Alert.created_at)
        )

        return self.db.scalars(statement).all()

    # GET ALERTS FOR A LISTING
    def get_by_listing(self, listing_id):

        statement = (
            select(Alert)
            .where(Alert.listing_id == listing_id)
            .order_by(desc(Alert.created_at))
        )

        return self.db.scalars(statement).all()

    # GET UNREAD ALERTS
    def get_unread(self):

        statement = (
            select(Alert)
            .where(Alert.is_read == False)
            .order_by(desc(Alert.created_at))
        )

        return self.db.scalars(statement).all()

    # MARK ALERT AS READ
    def mark_as_read(self, alert_id):

        alert = self.get_by_id(alert_id)

        if alert is None:
            return False

        try:
            alert.is_read = True

            self.db.commit()
            self.db.refresh(alert)

            return True

        except Exception:
            self.db.rollback()
            raise

    # DELETE
    def delete(self, alert_id):

        alert = self.get_by_id(alert_id)

        if alert is None:
            return False

        try:
            self.db.delete(alert)
            self.db.commit()

            return True

        except Exception:
            self.db.rollback()
            raise