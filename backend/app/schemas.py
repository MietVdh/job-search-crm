from sqlalchemy.orm import declarative_base
from typing import Annotated
from pydantic import BaseModel, ConfigDict, Field, HttpUrl, PlainSerializer

from datetime import date, datetime

DateOnly = Annotated[
    datetime,
    PlainSerializer(lambda dt: dt.date(), return_type=date)
]

class JobPostingResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    company: str
    url: str
    saved_at: DateOnly
    location: str | None 
    salary: str | None
    note: str | None 
    cover_letter_required: bool


class JobPostingListResponse(BaseModel):
    items: list[JobPostingResponse]
    page: int = Field(gt=0)
    page_size: int = Field(gt=0)
    total: int = Field(ge=0)


class JobPostingCreate(BaseModel):
    title: str = Field(max_length=200)
    company: str = Field(max_length=200)
    url: HttpUrl
    location: str | None = Field(default=None, max_length=200)
    salary: str | None = Field(default=None, max_length=100)
    note: str | None = None
    cover_letter_required: bool = False