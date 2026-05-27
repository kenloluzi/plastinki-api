from flask import Blueprint, request, jsonify
from sqlalchemy import or_
from app.models import Record

records_bp = Blueprint("records", __name__)


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

    if genre:
        q = q.filter(Record.genre == genre)
    if artist:
        q = q.filter(Record.artist.ilike(f"%{artist}%"))
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

    items = q.all()
    return jsonify({"items": [r.to_dict() for r in items], "count": len(items)})


@records_bp.get("/facets")
def facets():
    genres = [g[0] for g in Record.query.with_entities(Record.genre).distinct().all() if g[0]]
    artists = [a[0] for a in Record.query.with_entities(Record.artist).distinct().all() if a[0]]
    years = [y[0] for y in Record.query.with_entities(Record.year).distinct().all() if y[0]]
    return jsonify({
        "genres": sorted(genres),
        "artists": sorted(artists),
        "years": sorted(years),
    })


@records_bp.get("/<int:record_id>")
def get_record(record_id):
    record = Record.query.get_or_404(record_id)
    return jsonify(record.to_dict())
