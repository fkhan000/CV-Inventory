from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from business_logic.item_manager import ItemManager
from business_logic.item_tag_manager import ItemTagManager

def create_item_blueprint(engine):
    item_manager = ItemManager(engine)
    item_tag_manager = ItemTagManager(engine)

    item_bp = Blueprint("item_bp", __name__)

    @item_bp.route("/api/log_item", methods=["POST"])
    @cross_origin(supports_credentials=True)
    def log_item():
        data = request.json()
        tag_data = data["tags"]
        item_data = data["item"]

        item_manager.register_item(item_data)
        for tag in tag_data:
            item_tag_manager.register(tag)
        
        return jsonify({"Message": "Successfully logged item"}), 200
    
    @item_bp.route("/api/remove_item", methods=["POST"])
    @cross_origin(supports_credentials=True)
    def remove_item():
        data = request.get_json()
        item_id = data["item_id"]
        item_manager.remove_item({"item_id": item_id})

        return jsonify({"Message": "Successfully removed item"}), 200
    
    @item_bp.route("/api/remove_item", methods=["GET"])
    @cross_origin(supports_credentials=True)
    def fetch_items_inventory():
        #TODO: Add offset and limit options for pagination
        inventory_id = request.args.get("inventory_id")
        items = item_manager.fetch(inventory_id=inventory_id)
        return items, 200
    
    @item_bp.route("/api/similarity_search", methods=["GET"])
    @cross_origin(supports_credentials=True)
    def similarity_search():
        user_id = request.args.get("user_id")
        limit = request.args.get("limit")
        offset = request.args.get("offset")
        modality = request.args.get("modality")
        query = request.args.get("query")

        item_ids = item_manager.similarity_search(query, user_id, offset, limit, modality)

        items = item_manager.fetch(item_id = item_ids)

        return items, 200
    
    
    @item_bp.route("/api/search_by_tags", methods=["GET"])
    @cross_origin(supports_credentials=True)
    def search_by_tags():
        #TODO: Make function for this in item_manager, needs offset, limit, etc.
        pass
        


