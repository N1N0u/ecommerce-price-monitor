from sqlalchemy import select
from sqlalchemy.orm import Session

from database.models import Product


class ProductRepository:

    def __init__(self, db: Session):
        self.db = db

    # CREATE
    def create(self, name, category=None, sku=None):

        product = Product(
            name=name,
            category=category,
            sku=sku
        )

        try:
            self.db.add(product)
            self.db.commit()
            self.db.refresh(product)

            return product

        except Exception:
            self.db.rollback()
            raise

    # READ: Get product by ID
    def get_by_id(self, product_id):

        return self.db.get(Product, product_id)

    # READ: Get all products
    def get_all(self):

        statement = select(Product).order_by(Product.id)

        return self.db.scalars(statement).all()

    # READ: Get product by SKU
    def get_by_sku(self, sku):

        statement = select(Product).where(
            Product.sku == sku
        )

        return self.db.scalar(statement)

    # UPDATE
    def update(self, product_id, **updates):

        product = self.get_by_id(product_id)

        if product is None:
            return None

        allowed_fields = {"name", "category", "sku"}

        try:

            for field, value in updates.items():

                if field not in allowed_fields:
                    raise ValueError(
                        f"Invalid product field: {field}"
                    )

                setattr(product, field, value)

            self.db.commit()
            self.db.refresh(product)

            return product

        except Exception:
            self.db.rollback()
            raise

    # DELETE
    def delete(self, product_id):

        product = self.get_by_id(product_id)

        if product is None:
            return False

        try:

            self.db.delete(product)
            self.db.commit()

            return True

        except Exception:
            self.db.rollback()
            raise