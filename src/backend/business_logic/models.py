from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    TIMESTAMP,
    ForeignKey,
    func,
    MetaData
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import os
from dotenv import load_dotenv

Base = declarative_base()

class User(Base):
    """
    Represents a user in the system.
    Each user can own multiple inventories.
    """
    __tablename__ = "user"

    user_id = Column(Integer, primary_key=True)
    user_name = Column(String, unique=True, nullable=False, index=True)
    email_address = Column(String, unique=True, nullable=False)

    inventories = relationship("Inventory", back_populates="user", cascade="all, delete")

    def __repr__(self):
        return f"<User(user_id={self.user_id}, user_name='{self.user_name}')>"


class Inventory(Base):
    """
    Represents an inventory belonging to a user.
    Each inventory can contain multiple items.
    """
    __tablename__ = "inventory"

    inventory_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.user_id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False, index=True)
    description = Column(String, default="", nullable=False)
    #TODO: Add default inventory image of a drawer
    image_url = Column(String, nullable=False, default="")
    created_at = Column(TIMESTAMP, default=func.now(), nullable=False)

    user = relationship("User", back_populates="inventories")
    items = relationship("Item", back_populates="inventory", cascade="all, delete")

    def __repr__(self):
        return f"<Inventory(inventory_id={self.inventory_id}, name='{self.name}')>"


class Item(Base):
    """
    Represents an item inside an inventory.
    Each item belongs to a single inventory and can have multiple tags.
    """
    __tablename__ = "item"

    item_id = Column(Integer, primary_key=True)
    inventory_id = Column(Integer, ForeignKey("inventory.inventory_id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False, index=True)
    description = Column(String, default="", nullable=False)
    #TODO: Add default ? image in rare case we don't have image of the item
    image_url = Column(String, nullable=False, default="default_item_image.png")
    created_at = Column(TIMESTAMP, default=func.now(), nullable=False)

    inventory = relationship("Inventory", back_populates="items")
    tags = relationship("Tag", secondary="itemtag", back_populates="items")

    def __repr__(self):
        return f"<Item(item_id={self.item_id}, name='{self.name}')>"


class Tag(Base):
    """
    Represents a tag that can be associated with multiple items.
    Example tags: 'electronics', 'fragile', 'perishable'
    """
    __tablename__ = "tag"

    tag_id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False, index=True)

    items = relationship("Item", secondary="itemtag", back_populates="tags")

    def __repr__(self):
        return f"<Tag(tag_id={self.tag_id}, name='{self.name}')>"


class ItemTag(Base):
    """
    Association table for many-to-many relationship between items and tags.
    Links items to their respective tags.
    """
    __tablename__ = "itemtag"

    item_id = Column(Integer, ForeignKey("item.item_id", ondelete="CASCADE"), primary_key=True)
    tag_id = Column(Integer, ForeignKey("tag.tag_id", ondelete="CASCADE"), primary_key=True)

    def __repr__(self):
        return f"<ItemTag(item_id={self.item_id}, tag_id={self.tag_id})>"


def initialize():

    env_path = os.path.join('..', '.env')
    load_dotenv(dotenv_path=env_path)

    POSTGRES_USER = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_DB = os.getenv("POSTGRES_DB")
    POSTGRES_HOST = os.getenv("POSTGRES_HOST")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT")

    DATABASE_URL = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

    engine = create_engine(DATABASE_URL)

    metadata = MetaData()
    metadata.reflect(bind=engine)
    metadata.drop_all(bind=engine)

    Base.metadata.create_all(engine)

if __name__ == "__main__":
    initialize()