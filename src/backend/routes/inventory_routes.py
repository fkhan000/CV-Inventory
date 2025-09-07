from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from business_logic.inventory_manager import InventoryManager

def create_inventory_blueprint(engine, error_codes):

    inventory_manager = InventoryManager(engine, error_codes)
    inventory_bp = Blueprint("inventory_bp", __name__)

    @inventory_bp.route("/api/create_inventory", methods=["POST"])
    @cross_origin(supports_credentials=True)
    def create_inventory():
        data = request.json()
        inventory_manager.register(data)
        return jsonify({"message": "Successfully created inventory."}), 200
    
    @inventory_bp.route("/api/get_user_inventories", methods=["GET"])
    @cross_origin(supports_credentials=True)
    def get_user_inventories():
        user_id = request.args.get("user_id")
        inventory_manager.fetch({"user_id":user_id})
        return inventory_manager

    return inventory_bp