from pathlib import Path
from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


DATABASE_PATH = Path(__file__).resolve().parent.parent.parent / "career_crm.db"

engine = create_engine(
    f"sqlite:///{DATABASE_PATH.as_posix()}", 
    echo=True
)


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    ac = dbapi_connection.autocommit
    dbapi_connection.autocommit = True
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

    dbapi_connection.autocommit = ac

SessionFactory = sessionmaker(engine)

def get_session():
    with SessionFactory() as session:
        yield session



class Base(DeclarativeBase):
    pass