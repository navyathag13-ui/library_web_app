"""
/api/loans  — read-only loan listing for the History view.

Endpoints:
  GET /api/loans   — all loans, filterable by status / resource_id / borrower search
"""
from flask import Blueprint, jsonify, request
from models import db, Loan, Resource

loans_bp = Blueprint("loans", __name__, url_prefix="/api")


@loans_bp.get("/loans")
def list_loans():
    query = db.session.query(Loan).join(Resource, Loan.resource_id == Resource.id)

    # Filter by status
    status = request.args.get("status", "").strip()
    if status in ("active", "returned", "overdue"):
        query = query.filter(Loan.status == status)

    # Filter by resource
    resource_id = request.args.get("resource_id", "").strip()
    if resource_id.isdigit():
        query = query.filter(Loan.resource_id == int(resource_id))

    # Search borrower name or resource title
    search = request.args.get("search", "").strip()
    if search:
        like = f"%{search}%"
        query = query.filter(
            db.or_(Loan.borrower_name.ilike(like), Resource.title.ilike(like))
        )

    # Sort — newest first by default
    query = query.order_by(Loan.checkout_date.desc())

    # Pagination
    total    = query.count()
    page     = max(1, int(request.args.get("page", 1)))
    per_page = min(100, max(1, int(request.args.get("per_page", 20))))
    loans    = query.offset((page - 1) * per_page).limit(per_page).all()

    return jsonify({
        "loans":   [l.to_dict() for l in loans],
        "total":   total,
        "page":    page,
        "perPage": per_page,
        "pages":   max(1, -(-total // per_page)),
    }), 200
