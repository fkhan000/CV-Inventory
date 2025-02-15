# Database Models (SQLAlchemy)

This document provides an overview of the SQLAlchemy models used in the inventory system.

---

## **User Model**
Represents a registered user in the system. A user can own multiple inventories.

### **Table: `user`**
| Column Name   | Type      | Constraints             | Description                     |
|--------------|----------|------------------------|---------------------------------|
| user_id      | Integer  | Primary Key            | Unique ID for the user         |
| user_name    | String   | Unique, Not Null, Indexed | Username of the user           |
| email_address | String  | Unique, Not Null | Email address of the user      |

### **Relationships**
- A `User` **has many** `Inventories` (one-to-many).

### **Example Query**
```python
# Get all inventories for a user
user = session.query(User).filter_by(user_name="johndoe").first()
print(user.inventories)  # Lists all inventories owned by the user
```

---

## **Inventory Model**
Represents an inventory owned by a user. Each inventory contains multiple items.

### **Table: `inventory`**
| Column Name   | Type      | Constraints           | Description                          |
|--------------|----------|----------------------|--------------------------------------|
| inventory_id | Integer  | Primary Key          | Unique ID for the inventory         |
| user_id      | Integer  | Foreign Key (`user.user_id`), Not Null | Owner of the inventory |
| name         | String   | Not Null, Indexed    | Name of the inventory               |
| description  | String   | Default: ""         | Description of the inventory        |
| image_url    | String   | Default: "default_inventory_image.png" | URL for the inventory image |
| created_at   | TIMESTAMP | Default: `func.now()` | Timestamp when the inventory was created |

### **Relationships**
- An `Inventory` **belongs to** a `User` (many-to-one).
- An `Inventory` **has many** `Items` (one-to-many).

### **Example Query**
```python
# Fetch an inventory by name
inventory = session.query(Inventory).filter_by(name="Electronics").first()
print(inventory.items)  # Lists all items in this inventory
```

---

## **Item Model**
Represents an item stored in an inventory.

### **Table: `item`**
| Column Name   | Type      | Constraints           | Description                          |
|--------------|----------|----------------------|--------------------------------------|
| item_id      | Integer  | Primary Key          | Unique ID for the item              |
| inventory_id | Integer  | Foreign Key (`inventory.inventory_id`), Not Null | Inventory this item belongs to |
| name         | String   | Not Null, Indexed    | Name of the item                    |
| description  | String   | Default: ""         | Description of the item             |
| image_url    | String   | Default: "default_item_image.png" | URL for the item image |
| created_at   | TIMESTAMP | Default: `func.now()` | Timestamp when the item was added |

### **Relationships**
- An `Item` **belongs to** an `Inventory` (many-to-one).
- An `Item` **can have multiple** `Tags` (many-to-many).

### **Example Query**
```python
# Fetch all tags for an item
item = session.query(Item).filter_by(name="Laptop").first()
print(item.tags)  # Shows all tags associated with the item
```

---

## **Tag Model**
Represents a tag used to categorize items.

### **Table: `tag`**
| Column Name | Type    | Constraints           | Description                  |
|------------|--------|----------------------|------------------------------|
| tag_id     | Integer | Primary Key          | Unique ID for the tag        |
| name       | String  | Unique, Not Null, Indexed | Name of the tag (e.g., "Electronics") |

### **Relationships**
- A `Tag` **can be associated with multiple** `Items` (many-to-many).

### **Example Query**
```python
# Fetch all items with a specific tag
tag = session.query(Tag).filter_by(name="electronics").first()
print(tag.items)  # Lists all items with the 'electronics' tag
```

---

## **ItemTag Model (Association Table)**
A join table that establishes a **many-to-many relationship** between `Item` and `Tag`.

### **Table: `itemtag`**
| Column Name | Type      | Constraints                                   | Description                          |
|------------|----------|----------------------------------------------|--------------------------------------|
| item_id    | Integer  | Foreign Key (`item.item_id`), Primary Key, CASCADE Delete | ID of the linked item |
| tag_id     | Integer  | Foreign Key (`tag.tag_id`), Primary Key, CASCADE Delete | ID of the linked tag |

### **Relationships**
- Links `Item` and `Tag` in a **many-to-many** relationship.

### **Example Query**
```python
# Add a new tag to an item
item = session.query(Item).filter_by(name="Laptop").first()
tag = session.query(Tag).filter_by(name="electronics").first()
item.tags.append(tag)
session.commit()
```

---

# **Relationships Overview**
📌 **One-to-Many**
- `User → Inventories`
- `Inventory → Items`

📌 **Many-to-Many**
- `Item ↔ Tags` (via `ItemTag`)

---

# **Indexing & Performance Considerations**
- Indexed frequently queried fields: `user_name`, `name` (for fast lookups).
- Used `ondelete="CASCADE"` for **automatic cleanup** when a user or inventory is deleted.
- Used **default images** (`default_inventory_image.png`, `default_item_image.png`) to ensure missing images don’t break the UI.

---

# **Summary**
- ✅ **Users own inventories**
- ✅ **Inventories contain items**
- ✅ **Items can have multiple tags**
- ✅ **Tags can be associated with multiple items**
- ✅ **Data is indexed for efficiency**


---

📌 **Need Help?**
For database-related issues, check the official [SQLAlchemy Documentation](https://docs.sqlalchemy.org/).