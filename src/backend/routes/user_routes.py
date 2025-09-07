from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from business_logic.user_manager import UserManager

def create_user_blueprint(engine, error_codes):
    user_manager = UserManager(engine, error_codes)

    user_bp = Blueprint("user_bp", __name__)

    @user_bp.route("/api/register_user", methods=["POST"])
    @cross_origin(supports_credentials=True)
    def register_user():
        """Endpoint to register a new user.
        Expects JSON data with user information. (user_id, user_name, email_address)

        Returns
        -------
            JSON response indicating success.
        """
        user_data = request.get_json()
        user_manager.register(user_data)

        return jsonify({
            "message": "Successfully created user!",
            }), 200
    
    @user_bp.route("/api/fetch_user", methods=["GET"])
    @cross_origin(supports_credentials=True)
    def fetch_user():
        user_data = request.get_json()
        if "user_id" in user_data:
            user_data = user_manager.fetch({"user_id":user_data["user_id"]})
        elif "email_address" in user_data:
            user_data = user_manager.fetch({"email_address":user_data["email_address"]})
        elif "user_name" in user_data:
            user_data = user_manager.fetch({"user_name":user_data["user_name"]})
        else:
            return jsonify({
                "message": "Invalid Argument"
            }), 400

        return user_data

    @user_bp.route("/api/remove_user", methods=["GET"])
    @cross_origin(supports_credentials=True)
    def remove_user():
        user_data = request.get_json()
        if "user_id" in user_data:
            user_manager.remove({"user_id":user_data["user_id"]})
        elif "email_address" in user_data:
            user_data = user_manager.remove({"email_address":user_data["email_address"]})
        elif "user_name" in user_data:
            user_data = user_manager.remove({"user_name":user_data["user_name"]})
        else:
            return jsonify({
                "message": "Invalid Argument"
            }), 400
    
    return user_bp