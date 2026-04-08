"""
/api/stats    — dashboard summary counts.
/api/activity — recent loan activity feed.
"""
from flask import Blueprint, jsonify
from models import db, Resource, Loan

stats_bp = Blueprint("stats", __name__, url_prefix="/api")


@stats_bp.get("/stats")
def get_stats():
    total       = Resource.query.count()
    available   = Resource.query.filter(Resource.available_copies > 0).count()
    checked_out = Resource.query.filter(Resource.available_copies == 0).count()
    overdue     = Loan.query.filter_by(status="overdue").count()

    # Count resources per category
    rows = (
        db.session.query(Resource.category, db.func.count(Resource.id))
        .group_by(Resource.category)
        .order_by(db.func.count(Resource.id).desc())
        .all()
    )
    categories = [{"name": cat, "count": cnt} for cat, cnt in rows]

    return jsonify({
        "total":      total,
        "available":  available,
        "checkedOut": checked_out,
        "overdue":    overdue,
        "categories": categories,
    }), 200


@stats_bp.get("/activity")
def get_activity():
    """Return the 15 most recent loan events for the dashboard activity feed."""
    recent = (
        Loan.query
        .order_by(Loan.checkout_date.desc())
        .limit(15)
        .all()
    )
    return jsonify({"activity": [l.to_dict() for l in recent]}), 200
