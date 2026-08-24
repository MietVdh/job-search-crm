from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase


DATABASE_PATH = Path(__file__).resolve().parent.parent.parent / "career_crm.db"

engine = create_engine(
    f"sqlite:///{DATABASE_PATH.as_posix()}", 
    echo=True
)


class Base(DeclarativeBase):
    pass