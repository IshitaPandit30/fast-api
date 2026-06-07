from sqlalchemy import Integer, String, Column, Boolean, DateTime, VARCHAR
from sqlalchemy.orm import Mapped, mapped_column
from ..db import Base
from datetime import datetime, timezone

class CreateUserSchema(Base):
    __tablename__ ="users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    name = Column(VARCHAR(100), nullable=False)

    email= Column(VARCHAR(191), nullable=False, unique=True)

    password = Column(String, nullable=False)

    created_at= Column(DateTime, nullable=False, default=datetime.now(timezone.utc))

    updated_at= Column(DateTime, nullable=True, onupdate=datetime.now(timezone.utc))