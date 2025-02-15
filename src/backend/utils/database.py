from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.inspection import inspect

def create_session(engine) -> Session:
    """Creates a SQLAlhemy session"""
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


def object_as_dict(obj):
    """Converts a SQLAlchemy model instance into a dictionary."""

    return {c.key: getattr(obj, c.key) for c in inspect(obj).mapper.column_attrs}

