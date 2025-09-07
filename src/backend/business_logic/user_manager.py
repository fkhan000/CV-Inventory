from database.models import User
from .manager import Manager

class UserManager(Manager):

    def __init__(self, engine, error_codes):
        super().__init__(engine, User, error_codes)