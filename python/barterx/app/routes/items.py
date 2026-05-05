from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import db, Item

items_bp = Blueprint("items", __name__, url_prefix="/items")

@items_bp.route('/', methods=['GET'])
def get_items():
    items = Item.query.order_by(Item.created_at.desc()).all()

    return jsonify([
        {
            "id": i.id,
            "title": i.title,
            "price": i.price,
            "image": i.image if i.image else None,
            "created_at": i.created_at.strftime("%Y-%m-%d %H:%M:%S") if i.created_at else None
        }
        for i in items
    ])

@items_bp.route('/add', methods=['POST'])
@jwt_required()
def add_item():
    user_id = get_jwt_identity()
    data = request.form

    item = Item(
        user_id=user_id,
        title=data['title'],
        category=data['category'],
        price=data['price'],
        image=""
    )

    db.session.add(item)
    db.session.commit()

    return jsonify({"msg": "Item added"})

@items_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_item(id):
    item = Item.query.get(id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({"msg": "Deleted"})