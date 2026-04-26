from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from db import Base

class APIKey(Base):
    __tablename__ = "api_keys"

    id = Column(Integer, primary_key=True, index=True)
    key_hash = Column(String, unique=True, index=True, nullable=False)
    user_email = Column(String, index=True, nullable=False)
    credits = Column(Integer, default=0, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    transactions = relationship("Transaction", back_populates="api_key")
    usage_logs = relationship("UsageLog", back_populates="api_key")

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    api_key_id = Column(Integer, ForeignKey("api_keys.id"), nullable=True)
    user_email = Column(String, index=True, nullable=False)
    reference = Column(String, unique=True, index=True, nullable=False)
    payment_method = Column(String, nullable=False) # 'paypal' or 'akbank'
    amount = Column(Float, nullable=False)
    currency = Column(String, default="USD", nullable=False)
    status = Column(String, default="pending", nullable=False) # 'pending', 'verified', 'rejected'
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    api_key = relationship("APIKey", back_populates="transactions")

class UsageLog(Base):
    __tablename__ = "usage_logs"

    id = Column(Integer, primary_key=True, index=True)
    api_key_id = Column(Integer, ForeignKey("api_keys.id"), nullable=False)
    endpoint = Column(String, nullable=False)
    credits_used = Column(Integer, default=1, nullable=False)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    api_key = relationship("APIKey", back_populates="usage_logs")
