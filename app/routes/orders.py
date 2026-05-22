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
        # Проверка остатков
        if record.stock < qty:
            return jsonify({"error": f"Not enough stock for '{record.title}' by {record.artist}. Available: {record.stock}"}), 400
        line_total = float(record.price) * qty
        total += line_total
        order_items.append(OrderItem(
            record_id=record.id,
            quantity=qty,
            price=record.price,
            title_snapshot=record.title,
            artist_snapshot=record.artist,
        ))

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
    # Уменьшаем stock для каждой позиции
    for entry in items:
        rid = int(entry.get("record_id"))
        qty = max(1, int(entry.get("quantity", 1)))
        record = Record.query.get(rid)
        if record:
            record.stock -= qty
    db.session.commit()

    return jsonify(order.to_dict()), 201