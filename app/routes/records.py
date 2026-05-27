@records_bp.get("")
def list_records():
    q = Record.query

    genre = request.args.get("genre")
    artist = request.args.get("artist")
    year_min = request.args.get("year_min", type=int)
    year_max = request.args.get("year_max", type=int)
    price_min = request.args.get("price_min", type=float)
    price_max = request.args.get("price_max", type=float)
    search = request.args.get("search")
    sort = request.args.get("sort", "newest")
    condition = request.args.get("condition")

    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 12, type=int)

    if genre:
        q = q.filter(Record.genre == genre)
    if artist:
        q = q.filter(Record.artist.ilike(f"%{artist}%"))
    if condition:
        q = q.filter(Record.condition == condition)
    if year_min is not None:
        q = q.filter(Record.year >= year_min)
    if year_max is not None:
        q = q.filter(Record.year <= year_max)
    if price_min is not None:
        q = q.filter(Record.price >= price_min)
    if price_max is not None:
        q = q.filter(Record.price <= price_max)
    if search:
        like = f"%{search}%"
        q = q.filter(or_(Record.title.ilike(like), Record.artist.ilike(like)))

    if sort == "price_asc":
        q = q.order_by(Record.price.asc())
    elif sort == "price_desc":
        q = q.order_by(Record.price.desc())
    elif sort == "year_desc":
        q = q.order_by(Record.year.desc().nullslast())
    else:
        q = q.order_by(Record.created_at.desc())

    paginated = q.paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        "items": [r.to_dict() for r in paginated.items],
        "count": paginated.total,
        "page": paginated.page,
        "pages": paginated.pages,
        "per_page": paginated.per_page,
        "has_next": paginated.has_next,
        "has_prev": paginated.has_prev,
    })