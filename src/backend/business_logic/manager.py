from typing import TypeVar, Generic, Type, Dict, Any
from utils.database import create_session, object_as_dict
from functools import wraps
from sqlalchemy import exc
import psycopg2

T = TypeVar("T")

class Manager(Generic[T]):

    def __init__(self, engine, model: Type[T], error_codes: Dict[str, Any]):
        self.engine = engine
        self.model = model
        self.error_codes = error_codes
    
    @staticmethod
    def session_management(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            session = create_session(self.engine)
            try:
                result = func(self, session, *args, **kwargs)
                session.commit()
                return result
            except exc.IntegrityError as e:
                if isinstance(e.orig, psycopg2.errors.UniqueViolation):
                    constraint_name = e.orig.diag.constraint_name
                    column_name = e.orig.diag.column_name
                    raise Exception(
                        f"A {column_name} with that {constraint_name} already exists!",
                        self.error_codes[f"AlreadyExists"]
                    ) from e
                else:
                    raise Exception("An integrity error occurred.", 
                                    self.error_codes["IntegrityError"]) from e
            except Exception as e:
                raise Exception(
                    "An error occurred while accessing the database.",
                    self.error_codes["DatabaseError"]
                ) from e
            finally:
                session.close()
        return wrapper

    @session_management
    def register(self, session, data: Dict[str, Any], post_commit_callback = None):
        """Generic method to register a new record in the database."""
        new_object = self.model(**data)
        session.add(new_object)
        session.flush()

        registered_object = object_as_dict(new_object)

        if post_commit_callback:
            post_commit_callback(registered_object)

    @session_management
    def fetch(self, session, **filters) -> T:
        conditions = [
            getattr(self.model, key).in_(value) if isinstance(value, list) else getattr(self.model, key) == value
            for key, value in filters.items()
            ]
        result = session.query(self.model).filter(*conditions).all()
        
        if result is None:
            raise Exception(
                f"No record found in {self.model.__name__} with {filters}",
                self.error_codes[f"NotFound"]
            )
        if isinstance(result, list):
            result = [object_as_dict(re) for re in result]
            return result
        return object_as_dict(result)
    
    @session_management
    def remove(self, session, post_commit_callback=None, **filters) -> None:
        obj = self.fetch(session, **filters)
        session.delete(obj)
        if post_commit_callback:
            obj_data = object_as_dict(obj)
            post_commit_callback(obj_data)
    

    @session_management
    def update(self, session, filters: Dict[str, Any], updates: Dict[str, Any], post_commit_callback=None):
        """Generic method to update a record based on given filters."""
        obj = self.fetch(session, **filters)
        for key, value in updates.items():
            if hasattr(obj, key):
                setattr(obj, key, value)
        if post_commit_callback:
            post_commit_callback(updates)