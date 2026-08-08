from app.database import Base
from sqlalchemy import ForeignKey, Integer, String, Boolean, DateTime
from typing import List
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column , relationship

class User(Base):
    __tablename__ = "users"
    id = Mapped[int] = mapped_column(Integer, primary_key=True)
    email = Mapped[str] = mapped_column(String, unique=True)
    hashed_password = Mapped[str] = mapped_column(String)
    created_at = Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    notes = Mapped[List["Note"]] = relationship(back_populates="owner")

class Note(Base):
    __tablename__ = "notes"
    title = Mapped[str] = mapped_column(String)
    id = Mapped[int] = mapped_column(Integer, primary_key=True)
    content = Mapped[str] = mapped_column(String)
    favourite = Mapped[bool] = mapped_column(Boolean, default=False)
    created_at = Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    owner_id = Mapped[int] = mapped_column(ForeignKey("users.id"))
    owner: Mapped["User"] = relationship(back_populates="notes")
