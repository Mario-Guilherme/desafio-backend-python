from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

database_url = "postgresql://admin:admin@localhost:5432/"

engine = create_engine(database_url)
db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    from biblioteca.models import Biblioteca

    Base.metadata.create_all(bind=engine)
