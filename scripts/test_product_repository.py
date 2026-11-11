from uuid import uuid4

from database.connection import SessionLocal
from database.repositories.product_repository import ProductRepository


def main():

    db = SessionLocal()

    repository = ProductRepository(db)

    try:

        # CREATE
        unique_sku = f"TEST-{uuid4().hex[:8]}"

        product = repository.create(
            name="Gaming Mouse",
            category="Electronics",
            sku=unique_sku
        )

        print("\nProduct created:")
        print(product.id, product.name, product.sku)

        # READ BY ID
        found_product = repository.get_by_id(product.id)

        print("\nProduct retrieved:")
        print(found_product.name)

        # UPDATE
        updated_product = repository.update(
            product.id,
            name="Wireless Gaming Mouse"
        )

        print("\nProduct updated:")
        print(updated_product.name)

        # READ ALL
        products = repository.get_all()

        print("\nAll products:")

        for item in products:
            print(item.id, item.name)

        # DELETE
        deleted = repository.delete(product.id)

        print("\nProduct deleted:", deleted)

    finally:
        db.close()


if __name__ == "__main__":
    main()