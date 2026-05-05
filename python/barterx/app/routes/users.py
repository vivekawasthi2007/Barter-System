from flask import Blueprint, jsonify
from ..models import User

users_bp = Blueprint("users", __name__, url_prefix="/users")

@users_bp.route('/')
def get_users():
    users = User.query.all()
    return jsonify([{
        "id": u.id,
        "email": u.email,
        "contact": u.contact
    } for u in users])