from pymilvus import (
    MilvusClient,
    FieldSchema,
    CollectionSchema,
    DataType,
    Collection,
    connections
)
import os, json


class VDB_Loader:

    def __init__(self):
        self.db_client = MilvusClient(uri="http://localhost:19530", token="root:Milvus")

        schema_file = os.path.join("..", "..", "..", "config", "vdb_schema.json")
        with open(schema_file) as f:
            self.schema = json.load(f)
        
        data_type_map = {"int64": DataType.INT64,
                         "float_vector": DataType.FLOAT_VECTOR,
                         "string": DataType.STRING,
                         "timestamp": DataType.INT64}
        
        for _, collection_schema in self.schema.items():

            for field in collection_schema["field_args"]:
                dtype = field["dtype"]
                field["dtype"] = data_type_map[dtype]

    def create_collection(self, collection_name, description, field_args):

        index_params = {
            "index_type": "IVF_FLAT",
            "metric_type": "IP",
            "params": {"nlist": 128},
        }

        fields = [FieldSchema(**field) for field in field_args]

        connections.connect(
            alias="default",
            host="127.0.0.1",
            port="19530")
        schema = CollectionSchema(fields, description)
        collection = Collection(name=collection_name, schema=schema)

        for field in field_args:
            if field["dtype"] == DataType.FLOAT_VECTOR:
                collection.create_index(field_name = field["name"], index_params=index_params)
        

    
    def load_db(self):
        for collection_name, collection_schema in self.schema.items():
            if self.db_client.has_collection(collection_name):
                self.db_client.drop_collection(collection_name, timeout=60)

            self.create_collection(collection_name, 
                                   collection_schema["description"], 
                                   collection_schema["field_args"])

            self.db_client.close()
        

if __name__ == "__main__":
    vdb_loader = VDB_Loader()
    vdb_loader.load_db()