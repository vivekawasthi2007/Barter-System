from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from ..models import db, User

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json

    user = User(
        email=data['email'],
        password=generate_password_hash(data['password']),
        contact=data.get('contact')
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({"msg": "Registered"})

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json

    user = User.query.filter_by(email=data['email']).first()

    if user and check_password_hash(user.password, data['password']):
        token = create_access_token(identity=user.id)
        return jsonify({"status": "success","token": token, "user_id": user.id})

    return jsonify({"status": "error","msg": "Invalid credentials"}), 401