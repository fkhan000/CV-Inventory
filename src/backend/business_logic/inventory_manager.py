from database.models import Inventory
from manager import Manager

class InventoryManager(Manager):

    def __init__(self, engine, error_codes):
        super().__init__(engine, Inventory, error_codes)