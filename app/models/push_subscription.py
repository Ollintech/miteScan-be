from sqlalchemy import Column, Integer, String, Text, DateTime
from db.database import Base
from datetime import datetime

class PushSubscription(Base):
    __tablename__ = 'push_subscriptions'

    id = Column(Integer, primary_key=True)
    account = Column(String(50), nullable=True, index=True)
    user_email = Column(String(100), nullable=True)
    endpoint = Column(Text, unique=True, nullable=False)
    p256dh = Column(Text, nullable=False)
    auth = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
