from database.models import ItemTag
from manager import Manager

class ItemTagManager(Manager):

    def __init__(self, engine, error_codes):
        super().__init__(engine, ItemTag, error_codes)