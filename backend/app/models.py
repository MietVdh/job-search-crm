from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, DateTime, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base



class JobPosting(Base):
    __tablename__ = "job_postings"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    company: Mapped[str] = mapped_column(String(200))
    url: Mapped[str] = mapped_column(String(1000), unique=True)
    saved_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    location: Mapped[Optional[str]] = mapped_column(String(200))
    salary: Mapped[Optional[str]] = mapped_column(String(100))
    note: Mapped[Optional[str]] = mapped_column(Text)
    cover_letter_required: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        server_default="false"
    )


