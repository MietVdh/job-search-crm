from sqlalchemy.orm import declarative_base
from typing import Annotated
from pydantic import BaseModel, ConfigDict, PlainSerializer

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

