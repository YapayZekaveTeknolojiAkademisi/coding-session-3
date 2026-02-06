import uuid
from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone, timedelta
from database import Base

MINUTES = 5

def generate_id():
    return str(uuid.uuid4())

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True, default=generate_id)
    email = Column(String, unique=True, index=True)
    password = Column(String)

    sessions = relationship("SessionTable", back_populates="user")

class SessionTable(Base):
    __tablename__ = "sessions"
    
    id = Column(String, primary_key=True, index=True, default=generate_id)
    user_id = Column(String, ForeignKey("users.id"), index=True)

    token_jti = Column(String, unique=True, index=True, nullable=False)
    token_type = Column(String, nullable=False) # access or refresh
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    expires_at = Column(DateTime, default=lambda: datetime.now(timezone.utc) + timedelta(minutes=MINUTES))
    revoked_at = Column(DateTime, nullable=True)
    last_used = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="sessions")
