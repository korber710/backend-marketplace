from flask import Flask, jsonify, request

from .database import DatabaseManager


class MarketplaceAPI:
    def __init__(self, db: DatabaseManager):
        self.db = db
        self.app = Flask("Marketplace API")
        self._setup_routes()

    def _setup_routes(self):
        self.app.add_url_rule(
            "/api/buyers/register",
            "register_buyer",
            self.register_buyer,
            methods=["POST"],
        )
        self.app.add_url_rule(
            "/api/sellers/register",
            "register_seller",
            self.register_seller,
            methods=["POST"],
        )
        self.app.add_url_rule(
            "/api/buyers/login", "login_buyer", self.login_buyer, methods=["POST"]
        )
        self.app.add_url_rule(
            "/api/sellers/login", "login_seller", self.login_seller, methods=["POST"]
        )

    def register_buyer(self):
        data = request.get_json()
        user_id = self.db.create_user(data["name"], data["email"], "buyer")
        return jsonify({"id": user_id, "message": "User registered successfully"}), 201

    def register_seller(self):
        data = request.get_json()
        user_id = self.db.create_user(data["name"], data["email"], "seller")
        return jsonify({"id": user_id, "message": "User registered successfully"}), 201

    def login_buyer(self):
        data = request.get_json()
        user_data = self.db.get_user(data["email"])
        return jsonify({"id": user_data[0], "name": user_data[1], "email": user_data[2], "role": user_data[3]}), 200

    def login_seller(self):
        data = request.get_json()
        user_data = self.db.get_user(data["email"])
        return jsonify({"id": user_data[0], "name": user_data[1], "email": user_data[2], "role": user_data[3]}), 200
