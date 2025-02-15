from typing import Dict, Any
from database.models import Item
from manager import Manager
from pymilvus import MilvusClient, Collection
from services.embedding_model import EmbeddingModel
from datetime import datetime, timezone

class ItemManager(Manager):

    def __init__(self, engine, error_codes, vdb_client: MilvusClient):
        super().__init__(engine, Item, error_codes)
        self.vdb_client = vdb_client
        self.embedding_model = EmbeddingModel()
    
    def upsert(self, item_data: Dict[str, Any]):

        vector_fields = self.vdb_client.query(
            collection_name="items", 
            expr=f"item_id == {item_data['item_id']}",
            output_fields=["item_id", "timestamp", "inventory_id", "image_embedding", "text_embedding"]
        )

        vector_fields = vector_fields[0] if vector_fields else {}

        if vector_fields == {}:
            vector_fields = {k:item_data[k] for k in ("item_id", "timestamp", "inventory_id")}
            dt = datetime.now(timezone.utc)
            vector_fields["timestamp"] = int(dt.timestamp())

        if "image_url" in item_data:
            vector_fields["image_embedding"] =  self.embedding_model.embed_image(item_data["image_url"])
        if "description" in item_data:
            vector_fields["text_embedding"] =  self.embedding_model.embed_text(item_data["description"])
        
        self.vdb_client.upsert("items", vector_fields)
    
    def similarity_search(self, query: str, user_id, offset, num_neighbors, modality) -> Dict[str, Any]:
        search_params = {"metric_type": self.params["metric_type"], "params": {}}
        collection = Collection("Image")

        if modality == "image":
            query_vector = self.embedding_model.embed_image(query)
            anns_field = "image_embedding"
        else:
            query_vector = self.embedding_model.embed_text(query)
            anns_field = "text_embedding"

        res = collection.search(
                                data=[query_vector],
                                anns_field=anns_field,
                                expr=f"user_id == {user_id}",
                                limit=num_neighbors,
                                offset=offset,
                                param=search_params)[0]
        res = [re.item_id for re in res]
        return res

    @Manager.session_management
    def register_item(self, session, data):
        if "description" not in data:
            description = self.embedding_model.generate_description(data["image_url"])
            data["description"] = description
        self.register(session, data, post_commit_callback=self.upsert)
    
    @Manager.session_management
    def update_item(self, session, filters: Dict[str, Any], updates:Dict[str, Any]):
        post_commit_callback = None
        if "image_url" in updates or "description" in updates:
            post_commit_callback = self.upsert

        self.update(session, filters, updates, post_commit_callback=post_commit_callback)
    
    @Manager.session_management
    def remove_item(self, session, **filters):
        remove = lambda data: self.vdb_client.delete("items", ids=[data["item_id"]])
        self.remove(session, post_commit_callback=remove, **filters)