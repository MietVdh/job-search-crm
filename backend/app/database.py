from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


DATABASE_PATH = Path(__file__).resolve().parent.parent.parent / "career_crm.db"

engine = create_engine(
    f"sqlite:///{DATABASE_PATH.as_posix()}", 
    echo=True
)


SessionFactory = sessionmaker(engine)


class Base(DeclarativeBase):
    pass