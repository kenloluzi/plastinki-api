from functools import wraps
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models import User, Record, Order

admin_bp = Blueprint("admin", __name__)


def admin_required(fn):
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        user = User.query.get(int(get_jwt_identity()))
        if not user or not user.is_admin:
            return jsonify({"error": "Admin access required"}), 403
        return fn(*args, **kwargs)
    return wrapper


@admin_bp.get("/records")
@admin_required
def list_records():
    items = Record.query.order_by(Record.created_at.desc()).all()
    return jsonify({"items": [r.to_dict() for r in items]})


@admin_bp.post("/records")
@admin_required
def create_record():
    data = request.get_json() or {}
    required = ["title", "artist", "price"]
    missing = [f for f in required if data.get(f) in (None, "")]
    if missing:
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

    record = Record(
        title=data.get("title"),
        artist=data.get("artist"),
        year=data.get("year"),
        genre=data.get("genre"),
        condition=data.get("condition", "new"),
        price=data.get("price"),
        stock=data.get("stock", 1),
        image_url=data.get("image_url"),
        description=data.get("description"),
    )
    db.session.add(record)
    db.session.commit()
    return jsonify(record.to_dict()), 201


@admin_bp.put("/records/<int:record_id>")
@admin_required
def update_record(record_id):
    record = Record.query.get_or_404(record_id)
    data = request.get_json() or {}
    for field in ("title", "artist", "year", "genre", "condition", "price", "stock", "image_url", "description"):
        if field in data:
            setattr(record, field, data[field])
    db.session.commit()
    return jsonify(record.to_dict())


@admin_bp.delete("/records/<int:record_id>")
@admin_required
def delete_record(record_id):
    record = Record.query.get_or_404(record_id)
    db.session.delete(record)
    db.session.commit()
    return jsonify({"deleted": record_id})


@admin_bp.get("/orders")
@admin_required
def list_orders():
    orders = Order.query.order_by(Order.created_at.desc()).all()
    return jsonify({"items": [o.to_dict() for o in orders]})


@admin_bp.put("/orders/<int:order_id>")
@admin_required
def update_order(order_id):
    order = Order.query.get_or_404(order_id)
    data = request.get_json() or {}
    if "status" in data:
        order.status = data["status"]
    db.session.commit()
    return jsonify(order.to_dict())
