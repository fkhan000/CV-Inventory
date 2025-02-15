from database.models import Tag
from manager import Manager

class TagManager(Manager):

    def __init__(self, engine, error_codes):
        super().__init__(engine, Tag, error_codes)