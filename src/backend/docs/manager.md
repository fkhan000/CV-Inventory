# Manager Classes Documentation

## Overview
This document describes the structure and functionality of the **Manager** classes used in the project. Each model in the schema has a corresponding **Manager** class, which serves as an interface between the SQL database and the application logic. These classes ensure proper interaction with the database and Milvus (for vector storage) while maintaining consistency across operations.

## Structure of Manager Classes

### **Base Manager Class (`Manager`)**
The `Manager` class is a **generic base class** designed to provide a consistent API for all model-specific managers. It implements common database operations, including:

- **Register**: Inserts a new record into the SQL database and optionally executes a post-commit callback.
- **Fetch**: Retrieves a record based on given filters.
- **Update**: Modifies existing records while ensuring any necessary updates (e.g., vector embeddings) are also applied.
- **Remove**: Deletes a record from the SQL database and optionally removes related entries from external storage (e.g., Milvus).

#### **Session Management Decorator (`session_management`)**
This decorator ensures that:
- A database session is created and properly managed.
- Transactions are committed only if no errors occur.
- The session is rolled back in case of failure to maintain database integrity.

### **Model-Specific Manager Classes**
Each model in the schema has its own `Manager` subclass that extends the base `Manager` and adds any model-specific logic.

#### **Example: `ItemManager`**
The `ItemManager` class extends `Manager[Item]` and is responsible for managing **Item** objects in both the SQL database and the Milvus vector database.

##### **Key Responsibilities**
1. **Upsert (`upsert`)**
   - Retrieves an existing record from Milvus.
   - If the record is missing, ensures that all required fields are provided.
   - Updates image/text embeddings when necessary.
   - Performs an upsert operation in Milvus to keep vector data in sync.

2. **Similarity Search (`similarity_search`)**
   - Uses embeddings to find similar items in Milvus.
   - Supports both **image-based** and **text-based** similarity search.

3. **Register Item (`register_item`)**
   - Registers an item in SQL.
   - Ensures that the corresponding vector is added to Milvus post-commit.

4. **Update Item (`update_item`)**
   - Updates SQL records.
   - If the `description` or `image_url` changes, the vector database is also updated.

5. **Remove Item (`remove_item`)**
   - Deletes an item from the SQL database.
   - Ensures the corresponding vector is removed from Milvus.

### **Embedding Model (`EmbeddingModel`)**
The `EmbeddingModel` class is responsible for generating embeddings for **text** and **images** using **Replicate API**. It also supports **image captioning**.

#### **Methods**
1. **`embed_image(image_url: str) -> list`**
   - Generates an embedding vector for an image.
   - Uses the `daanelson/imagebind` model.

2. **`embed_text(text: str) -> list`**
   - Converts a text string into an embedding vector.
   - Uses the same `daanelson/imagebind` model.

3. **`generate_description(image_url: str) -> str`**
   - Uses the `salesforce/blip` model to generate a text description (caption) for an image.
   - Strips the "Caption: " prefix from the output.

## **Conclusion**
The **Manager classes** provide a structured way to interact with both SQL and vector databases, ensuring **data consistency** and **efficient retrieval**. The **EmbeddingModel** integrates deep learning-based embeddings, enabling **semantic search** and **recommendation features** within the system.

By leveraging these classes, the project ensures:
- **Scalability**: Centralized database operations that can be extended for new models.
- **Consistency**: Synchronized updates between SQL and Milvus.
- **Efficiency**: Optimized similarity search and embedding generation.
