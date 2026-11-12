from sqlalchemy import select, desc
from sqlalchemy.orm import Session

from database.models import (
    ProductListing,
    PriceHistory,
    Alert
)


class PriceMonitorService:

    def __init__(self, db: Session):
        self.db = db

    def record_observation(
        self,
        listing_id,
        price,
        currency,
        availability,
        original_price=None
    ):

        # 1. Validate the new price
        if price <= 0:
            raise ValueError("Price must be greater than zero.")

        # 2. Check that the listing exists
        listing = self.db.get(
            ProductListing,
            listing_id
        )

        if listing is None:
            raise ValueError(
                f"Product listing {listing_id} does not exist."
            )

        # 3. Retrieve the previous observation
        statement = (
            select(PriceHistory)
            .where(PriceHistory.listing_id == listing_id)
            .order_by(
                desc(PriceHistory.scraped_at),
                desc(PriceHistory.id)
            )
            .limit(1)
        )

        previous = self.db.scalar(statement)

        alerts = []

        try:

            # 4. Detect price changes
            if previous is not None:

                if previous.currency == currency:

                    if price < previous.price:

                        difference = round(
                            previous.price - price,
                            2
                        )

                        alerts.append(
                            Alert(
                                listing_id=listing_id,
                                alert_type="price_drop",
                                old_value=str(previous.price),
                                new_value=str(price),
                                message=(
                                    f"Price decreased from "
                                    f"{previous.price} to {price} "
                                    f"{currency}. "
                                    f"Difference: {difference}."
                                )
                            )
                        )

                    elif price > previous.price:

                        difference = round(
                            price - previous.price,
                            2
                        )

                        alerts.append(
                            Alert(
                                listing_id=listing_id,
                                alert_type="price_increase",
                                old_value=str(previous.price),
                                new_value=str(price),
                                message=(
                                    f"Price increased from "
                                    f"{previous.price} to {price} "
                                    f"{currency}. "
                                    f"Difference: {difference}."
                                )
                            )
                        )

            # 5. Detect availability changes
            if previous is not None:

                old_availability = previous.availability.strip().lower()
                new_availability = availability.strip().lower()

                if old_availability != new_availability:

                    alert_type = "availability_change"

                    if (
                        "in stock" in new_availability
                        and "out of stock" not in new_availability
                    ):
                        alert_type = "back_in_stock"

                    elif (
                        "out of stock" in new_availability
                        or "sold out" in new_availability
                        or "unavailable" in new_availability
                    ):
                        alert_type = "out_of_stock"

                    alerts.append(
                        Alert(
                            listing_id=listing_id,
                            alert_type=alert_type,
                            old_value=previous.availability,
                            new_value=availability,
                            message=(
                                f"Availability changed from "
                                f"'{previous.availability}' to "
                                f"'{availability}'."
                            )
                        )
                    )

            # 6. Save the new price observation
            history = PriceHistory(
                listing_id=listing_id,
                price=price,
                original_price=original_price,
                currency=currency,
                availability=availability
            )

            self.db.add(history)

            # 7. Save generated alerts
            self.db.add_all(alerts)

            # 8. Commit everything together
            self.db.commit()

            self.db.refresh(history)

            return {
                "history": history,
                "alerts": alerts,
                "previous_observation": previous
            }

        except Exception:

            # Cancel all changes if something fails
            self.db.rollback()

            raise
