import os, json
from flask import Flask
from flask_cors import CORS
from sqlalchemy import create_engine
from load_dotenv import load_dotenv
from pymilvus import MilvusClient

from routes.inventory_routes import create_inventory_blueprint
from routes.item_routes import create_item_blueprint
from routes.user_routes import create_user_blueprint

app = Flask(__name__)
CORS(app, support_credentials=True)

load_dotenv()
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")


engine_str = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
engine = create_engine(
    engine_str,
    pool_size=500,
    max_overflow=200,
    pool_timeout=300,
)
milvus_client = MilvusClient(uri="http://localhost:19530", token="root:Milvus")

with open(os.path.join("..", "..", "config", "error_codes.json"), "r") as f:
    error_codes = json.load(f)

app.register_blueprint(create_user_blueprint(engine, error_codes))
app.register_blueprint(create_item_blueprint(engine, error_codes, error_codes, milvus_client))
app.register_blueprint(create_inventory_blueprint(engine, error_codes))


if __name__ == "__main__":
    app.run(debug=True)
