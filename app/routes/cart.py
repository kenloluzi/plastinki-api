from flask import Blueprint, request, jsonify
from app.models import Record

cart_bp = Blueprint("cart", __name__)


@cart_bp.post("/preview")
def preview():
    """Stateless cart preview: client sends [{record_id, quantity}], gets pricing back."""
    data = request.get_json() or {}
    items = data.get("items") or []

    if not isinstance(items, list):
        return jsonify({"error": "items must be a list"}), 400

    out = []
    total = 0.0

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
        out.append({
            "record_id": record.id,
            "title": record.title,
            "artist": record.artist,
            "price": float(record.price),
            "quantity": qty,
            "image_url": record.image_url,
            "line_total": round(line_total, 2),
            "in_stock": record.stock >= qty,
        })

    return jsonify({"items": out, "total": round(total, 2)})
