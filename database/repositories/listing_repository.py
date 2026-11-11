from sqlalchemy import select
from sqlalchemy.orm import Session

from database.models import ProductListing


class ListingRepository:

    def __init__(self, db: Session):
        self.db = db

    # CREATE
    def create(
        self,
        product_id,
        competitor_id,
        product_url,
        external_product_id=None
    ):

        listing = ProductListing(
            product_id=product_id,
            competitor_id=competitor_id,
            product_url=product_url,
            external_product_id=external_product_id
        )

        try:
            self.db.add(listing)
            self.db.commit()
            self.db.refresh(listing)

            return listing

        except Exception:
            self.db.rollback()
            raise

    # READ BY ID
    def get_by_id(self, listing_id):

        return self.db.get(ProductListing, listing_id)

    # READ ALL
    def get_all(self):

        statement = select(ProductListing).order_by(
            ProductListing.id
        )

        return self.db.scalars(statement).all()

    # GET LISTINGS FOR A PRODUCT
    def get_by_product(self, product_id):

        statement = select(ProductListing).where(
            ProductListing.product_id == product_id
        )

        return self.db.scalars(statement).all()

    # GET LISTINGS FOR A COMPETITOR
    def get_by_competitor(self, competitor_id):

        statement = select(ProductListing).where(
            ProductListing.competitor_id == competitor_id
        )

        return self.db.scalars(statement).all()

    # DELETE
    def delete(self, listing_id):

        listing = self.get_by_id(listing_id)

        if listing is None:
            return False

        try:
            self.db.delete(listing)
            self.db.commit()

            return True

        except Exception:
            self.db.rollback()
            raise