from sqlalchemy import (
    Column, String, Integer, Numeric, Boolean,
    Text, BigInteger, ForeignKey, DateTime
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func
from sqlalchemy import Column, String, Integer, Numeric, Boolean, Text, BigInteger, ForeignKey, DateTime, Date
from sqlalchemy.dialects.postgresql import UUID
import uuid

Base = declarative_base()

class Zone(Base):
    __tablename__ = "zones"
    id               = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name             = Column(String(100), nullable=False)
    city             = Column(String(100), nullable=False)
    boundary_geojson = Column(Text)
    population       = Column(Integer)
    created_at       = Column(DateTime(timezone=True), server_default=func.now())
    bins             = relationship("Bin", back_populates="zone")

class Bin(Base):
    __tablename__ = "bins"
    id             = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    zone_id        = Column(UUID(as_uuid=True), ForeignKey("zones.id"), nullable=False)
    bin_code       = Column(String(20), unique=True, nullable=False)
    latitude       = Column(Numeric(9, 6), nullable=False)
    longitude      = Column(Numeric(9, 6), nullable=False)
    capacity_liters= Column(Integer, default=120)
    bin_type       = Column(String(20), default="smart")
    is_active      = Column(Boolean, default=True)
    installed_at   = Column(DateTime(timezone=True), server_default=func.now())
    zone           = relationship("Zone", back_populates="bins")
    telemetry      = relationship("BinTelemetry", back_populates="bin")

class BinTelemetry(Base):
    __tablename__ = "bin_telemetry"
    id            = Column(BigInteger, primary_key=True, autoincrement=True)
    bin_id        = Column(UUID(as_uuid=True), ForeignKey("bins.id"), nullable=False)
    fill_level    = Column(Numeric(4, 3), nullable=False)
    detected_type = Column(String(20))
    confidence    = Column(Numeric(4, 3))
    is_hazardous  = Column(Boolean, default=False)
    temperature_c = Column(Numeric(4, 1))
    recorded_at   = Column(DateTime(timezone=True), server_default=func.now())
    bin           = relationship("Bin", back_populates="telemetry")

class User(Base):
    __tablename__ = "users"
    id            = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    zone_id       = Column(UUID(as_uuid=True), ForeignKey("zones.id"))
    name          = Column(String(100))
    phone         = Column(String(20), unique=True)
    role          = Column(String(20), default="citizen")
    reward_points = Column(Integer, default=0)
    created_at    = Column(DateTime(timezone=True), server_default=func.now())
    disposals = relationship("DisposalLog", back_populates="user")

class Alert(Base):
    __tablename__ = "alerts"
    id          = Column(BigInteger, primary_key=True, autoincrement=True)
    bin_id      = Column(UUID(as_uuid=True), ForeignKey("bins.id"), nullable=True)
    zone_id     = Column(UUID(as_uuid=True), ForeignKey("zones.id"), nullable=False)
    alert_type  = Column(String(30), nullable=False)
    severity    = Column(String(10), default="medium")
    message     = Column(Text)
    is_resolved = Column(Boolean, default=False)
    created_at  = Column(DateTime(timezone=True), server_default=func.now())

class DisposalEvent(Base):
    __tablename__ = "disposal_events"
    id            = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id       = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    bin_id        = Column(UUID(as_uuid=True), ForeignKey("bins.id"), nullable=True)  # ← change to True
    waste_type    = Column(String(20))
    was_correct   = Column(Boolean, default=False)
    points_earned = Column(Integer, default=0)
    disposed_at   = Column(DateTime(timezone=True), server_default=func.now())

class CollectionRoute(Base):
    __tablename__ = "collection_routes"
    id           = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    driver_id    = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    zone_id      = Column(UUID(as_uuid=True), ForeignKey("zones.id"), nullable=False)
    status       = Column(String(20), default="planned")
    planned_at   = Column(DateTime(timezone=True))
    started_at   = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    total_km     = Column(Numeric(6, 2))
    fuel_liters  = Column(Numeric(6, 2))

class WastePrediction(Base):
    __tablename__ = "waste_predictions"
    id             = Column(BigInteger, primary_key=True, autoincrement=True)
    zone_id        = Column(UUID(as_uuid=True), ForeignKey("zones.id"), nullable=False)
    predicted_for  = Column(Date, nullable=False)
    predicted_kg   = Column(Numeric(8, 2))
    waste_type     = Column(String(20))
    model_version  = Column(String(20))
    created_at     = Column(DateTime(timezone=True), server_default=func.now())

class DisposalLog(Base):
    __tablename__ = "disposal_logs"
    id            = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id       = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    bin_id        = Column(UUID(as_uuid=True), ForeignKey("bins.id"), nullable=True)
    waste_type    = Column(String(20), nullable=False)   # plastic,organic,metal,glass,hazardous
    is_correct    = Column(Boolean, default=True)
    points_earned = Column(Integer, default=0)
    confidence    = Column(Numeric(4,3))
    image_url     = Column(Text)
    recorded_at   = Column(DateTime(timezone=True), server_default=func.now())
    user          = relationship("User", back_populates="disposals")

class Badge(Base):
    __tablename__ = "badges"
    id          = Column(Integer, primary_key=True, autoincrement=True)
    code        = Column(String(30), unique=True, nullable=False)
    name        = Column(String(60), nullable=False)
    description = Column(Text)
    icon        = Column(String(10))
    points_req  = Column(Integer, default=0)
    scans_req   = Column(Integer, default=0)

class UserBadge(Base):
    __tablename__ = "user_badges"
    id         = Column(Integer, primary_key=True, autoincrement=True)
    user_id    = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    badge_id   = Column(Integer, ForeignKey("badges.id"), nullable=False)
    earned_at  = Column(DateTime(timezone=True), server_default=func.now())

class MarketplaceListing(Base):
    __tablename__ = "marketplace_listings"
    id            = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    seller_id     = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    waste_type    = Column(String(20), nullable=False)
    quantity_kg   = Column(Numeric(10, 2), nullable=False)
    base_price    = Column(Numeric(10, 2), nullable=False)
    current_price = Column(Numeric(10, 2))
    status        = Column(String(20), default="active")
    title         = Column(String(200))
    description   = Column(Text)
    location      = Column(String(100))
    expires_at    = Column(DateTime(timezone=True))
    created_at    = Column(DateTime(timezone=True), server_default=func.now())
    bids          = relationship("MarketplaceBid", back_populates="listing")

class MarketplaceBid(Base):
    __tablename__ = "marketplace_bids"
    id            = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    listing_id    = Column(UUID(as_uuid=True), ForeignKey("marketplace_listings.id"), nullable=False)
    bidder_id     = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    bid_amount    = Column(Numeric(10, 2), nullable=False)
    status        = Column(String(20), default="pending")
    note          = Column(Text)
    created_at    = Column(DateTime(timezone=True), server_default=func.now())
    listing       = relationship("MarketplaceListing", back_populates="bids")

class MarketplaceTransaction(Base):
    __tablename__ = "marketplace_transactions"
    id            = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    listing_id    = Column(UUID(as_uuid=True), ForeignKey("marketplace_listings.id"), nullable=False)
    seller_id     = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    buyer_id      = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    final_price   = Column(Numeric(10, 2), nullable=False)
    quantity_kg   = Column(Numeric(10, 2), nullable=False)
    status        = Column(String(20), default="completed")
    created_at    = Column(DateTime(timezone=True), server_default=func.now())