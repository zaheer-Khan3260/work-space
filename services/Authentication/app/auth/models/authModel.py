from app.db.database import Base
from sqlalchemy import Column, String, TIMESTAMP, Boolean, text, DateTime
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid

class Auth(Base):
    __tablename__ = 'usercredentials'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, server_default=text('gen_random_uuid()'))
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
