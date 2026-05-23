from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models import Order, OrderItem, Record, User

orders_bp = Blueprint("orders", __name__)


@orders_bp.post("")
@jwt_required()
def create_order():
    user_id = int(get_jwt_identity())
    data = request.get_json() or {}

    shipping = data.get("shipping") or {}
    items = data.get("items") or []

    required = ["full_name", "address", "city", "zip_code"]
    missing = [f for f in required if not shipping.get(f)]
    if missing:
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

    if not items:
        return jsonify({"error": "Cart is empty"}), 400

    # Проверка остатков
    for entry in items:
        try:
            rid = int(entry.get("record_id"))
            qty = max(1, int(entry.get("quantity", 1)))
        except (TypeError, ValueError):
            continue
        record = Record.query.get(rid)
        if not record:
            return jsonify({"error": f"Record {rid} not found"}), 400
        if record.stock < qty:
            return jsonify({"error": f"Not enough stock for {record.title} by {record.artist}. Available: {record.stock}"}), 400

    total = 0.0
    order_items = []
    for entry in items:
        try:
            rid = int(entry.get("record_id"))
            qty = max(1, int(entry.get("quantity", 1)))
        except (TypeError, ValueError):
            continue
        record = Record.query.get(rid)
        if not record:
            continue
        line_total = float(record.price) * qty
        total += line_total
        order_items.append(OrderItem(
            record_id=record.id,
            quantity=qty,
            price=record.price,
            title_snapshot=record.title,
            artist_snapshot=record.artist,
        ))
        record.stock -= qty

    if not order_items:
        return jsonify({"error": "No valid items in cart"}), 400

    order = Order(
        user_id=user_id,
        full_name=shipping.get("full_name"),
        address=shipping.get("address"),
        city=shipping.get("city"),
        zip_code=shipping.get("zip_code"),
        phone=shipping.get("phone"),
        total=round(total, 2),
        items=order_items,
    )
    db.session.add(order)
    db.session.commit()

    return jsonify(order.to_dict()), 201


@orders_bp.get("")
@jwt_required()
def list_my_orders():
    user_id = int(get_jwt_identity())
    orders = Order.query.filter_by(user_id=user_id).order_by(Order.created_at.desc()).all()
    return jsonify({"items": [o.to_dict() for o in orders]})


@orders_bp.get("/<int:order_id>")
@jwt_required()
def get_order(order_id):
    user_id = int(get_jwt_identity())
    order = Order.query.filter_by(id=order_id, user_id=user_id).first_or_404()
    return jsonify(order.to_dict())


@orders_bp.delete("/<int:order_id>")
@jwt_required()
def delete_order(order_id):
    user_id = int(get_jwt_identity())
    order = Order.query.get_or_404(order_id)
    user = User.query.get(user_id)

    if not (user.is_admin or order.user_id == user_id):
        return jsonify({"error": "You don't have permission to delete this order"}), 403

    db.session.delete(order)
    db.session.commit()
    return jsonify({"message": f"Order {order_id} deleted successfully"}), 200