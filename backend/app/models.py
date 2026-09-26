from datetime import datetime
from typing import Optional
import enum

from sqlalchemy import Boolean, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base



class JobPosting(Base):
    __tablename__ = "job_postings"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    company: Mapped[str] = mapped_column(String(200))
    url: Mapped[Optional[str]] = mapped_column(String(1000), unique=True)
    saved_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    location: Mapped[Optional[str]] = mapped_column(String(200))
    salary: Mapped[Optional[str]] = mapped_column(String(100))
    note: Mapped[Optional[str]] = mapped_column(Text)
    cover_letter_required: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        server_default="false"
    )
    application: Mapped[Optional["Application"]] = relationship(back_populates="job_posting")


class ApplicationStatus(enum.Enum):
    APPLIED = "applied"
    INVITED_TO_TEST = "invited_to_test"
    INTERVIEW = "interview"
    OFFER = "offer"
    REJECTED = "rejected"
    WITHDRAWN = "withdrawn"


class ApplicationMethod(enum.Enum):
    LINKEDIN = "LinkedIn"
    EMAIL = "email"
    COMPANY_WEBSITE = "company_website"
    REFERRAL = "referral"
    OTHER = "other"

class Application(Base):
    __tablename__ = "applications"

    id: Mapped[int] = mapped_column(primary_key=True)
    job_posting_id: Mapped[int] = mapped_column(
        ForeignKey("job_postings.id", ondelete="NO ACTION"), 
        unique=True
        )
    applied_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    how_applied: Mapped[ApplicationMethod] = mapped_column(default=ApplicationMethod.COMPANY_WEBSITE)
    status: Mapped[ApplicationStatus] = mapped_column(default=ApplicationStatus.APPLIED)
    last_response_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    job_posting: Mapped["JobPosting"] = relationship(back_populates="application")

