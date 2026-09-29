from typing import Annotated
from pydantic import AliasPath, BaseModel, ConfigDict, Field, HttpUrl, PlainSerializer

from datetime import date, datetime

from backend.app.models import ApplicationMethod, ApplicationStatus

DateOnly = Annotated[
    datetime,
    PlainSerializer(lambda dt: dt.date(), return_type=date)
]


class PaginatedResponse[T](BaseModel):
    items: list[T]
    page: int = Field(gt=0)
    page_size: int = Field(gt=0)
    total: int = Field(ge=0)



class JobPostingResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    company: str
    url: str | None
    saved_at: DateOnly
    location: str | None 
    salary: str | None
    note: str | None 
    cover_letter_required: bool


class JobPostingCreate(BaseModel):
    title: str = Field(max_length=200)
    company: str = Field(max_length=200)
    url: HttpUrl | None = None
    location: str | None = Field(default=None, max_length=200)
    salary: str | None = Field(default=None, max_length=100)
    note: str | None = None
    cover_letter_required: bool = False


class ApplicationListItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    job_posting_id: int

    job_title: str = Field(validation_alias=AliasPath("job_posting", "title"))
    company: str = Field(validation_alias=AliasPath("job_posting", "company"))

    applied_at: DateOnly
    how_applied: ApplicationMethod
    status: ApplicationStatus
    last_response_at: DateOnly | None


class ApplicationDetail(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    job_posting_id: int

    job_title: str = Field(validation_alias=AliasPath("job_posting", "title"))
    company: str = Field(validation_alias=AliasPath("job_posting", "company"))
    url: str | None = Field(validation_alias=AliasPath("job_posting", "url"))
    saved_at: DateOnly = Field(validation_alias=AliasPath("job_posting", "saved_at"))
    location: str | None = Field(validation_alias=AliasPath("job_posting", "location")) 
    salary: str | None = Field(validation_alias=AliasPath("job_posting", "salary"))
    note: str | None = Field(validation_alias=AliasPath("job_posting", "note"))
    cover_letter_required: bool = Field(validation_alias=AliasPath("job_posting", "cover_letter_required"))

    applied_at: DateOnly
    how_applied: ApplicationMethod
    status: ApplicationStatus
    last_response_at: DateOnly | None


class ApplicationCreate(BaseModel):
    job_posting_id: int
    how_applied: ApplicationMethod
    applied_at: date | None = None