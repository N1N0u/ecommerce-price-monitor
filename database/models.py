from datetime import datetime, timezone

from sqlalchemy import (
    String,
    Integer,
    Float,
    DateTime,
    ForeignKey,
    Boolean,
    UniqueConstraint,
    Index,
)

from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.connection import Base


def utc_now():
    return datetime.now(timezone.utc)


# ==========================================
# PRODUCTS
# ==========================================

class Product(Base):

    __tablename__ = "products"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    category: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    sku: Mapped[str | None] = mapped_column(
        String(100),
        unique=True,
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now
    )

    listings: Mapped[list["ProductListing"]] = relationship(
        back_populates="product",
        cascade="all, delete-orphan"
    )


# ==========================================
# COMPETITORS
# ==========================================

class Competitor(Base):

    __tablename__ = "competitors"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    website_url: Mapped[str] = mapped_column(
        String(500),
        unique=True,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now
    )

    listings: Mapped[list["ProductListing"]] = relationship(
        back_populates="competitor",
        cascade="all, delete-orphan"
    )


# ==========================================
# PRODUCT LISTINGS
# ==========================================

class ProductListing(Base):

    __tablename__ = "product_listings"

    __table_args__ = (
        UniqueConstraint(
            "competitor_id",
            "product_url",
            name="uq_competitor_product_url"
        ),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id"),
        nullable=False
    )

    competitor_id: Mapped[int] = mapped_column(
        ForeignKey("competitors.id"),
        nullable=False
    )

    product_url: Mapped[str] = mapped_column(
        String(1000),
        nullable=False
    )

    external_product_id: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now
    )

    product: Mapped["Product"] = relationship(
        back_populates="listings"
    )

    competitor: Mapped["Competitor"] = relationship(
        back_populates="listings"
    )

    price_history: Mapped[list["PriceHistory"]] = relationship(
        back_populates="listing",
        cascade="all, delete-orphan"
    )

    alerts: Mapped[list["Alert"]] = relationship(
        back_populates="listing",
        cascade="all, delete-orphan"
    )


# ==========================================
# PRICE HISTORY
# ==========================================

class PriceHistory(Base):

    __tablename__ = "price_history"

    __table_args__ = (
        Index("ix_price_listing_scraped", "listing_id", "scraped_at"),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    listing_id: Mapped[int] = mapped_column(
        ForeignKey("product_listings.id"),
        nullable=False
    )

    price: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    original_price: Mapped[float | None] = mapped_column(
        Float,
        nullable=True
    )

    currency: Mapped[str] = mapped_column(
        String(10),
        nullable=False
    )

    availability: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    scraped_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now
    )

    listing: Mapped["ProductListing"] = relationship(
        back_populates="price_history"
    )


# ==========================================
# ALERTS
# ==========================================

class Alert(Base):

    __tablename__ = "alerts"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    listing_id: Mapped[int] = mapped_column(
        ForeignKey("product_listings.id"),
        nullable=False
    )

    alert_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    old_value: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    new_value: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    message: Mapped[str] = mapped_column(
        String(1000),
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now
    )

    is_read: Mapped[bool] = mapped_column(
        Boolean,
        default=False
    )

    listing: Mapped["ProductListing"] = relationship(
        back_populates="alerts"
    )
