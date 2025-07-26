from sqlalchemy import Column, Integer, Numeric, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database import Base

class Movement(Base):
    __tablename__ = 'movements'

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Numeric(10, 2), nullable=False)
    type = Column(String(20), nullable=False)   # 'in' or 'out'
    description = Column(String(255))
    date = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationship with User
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="movements")