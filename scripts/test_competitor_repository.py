from database.connection import SessionLocal
from database.repositories.competitor_repository import CompetitorRepository


def main():

    db = SessionLocal()
    repository = CompetitorRepository(db)

    try:

        # CREATE
        competitor = repository.create(
            name="Demo Store A",
            website_url="https://demo-store-a.example.com"
        )

        print("\nCompetitor created:")
        print(competitor.id, competitor.name)

        # READ BY ID
        found = repository.get_by_id(competitor.id)

        print("\nCompetitor retrieved:")
        print(found.name)

        # READ ALL
        competitors = repository.get_all()

        print("\nAll competitors:")

        for item in competitors:
            print(item.id, item.name, item.website_url)

        # DELETE
        deleted = repository.delete(competitor.id)

        print("\nCompetitor deleted:", deleted)

    finally:
        db.close()


if __name__ == "__main__":
    main()