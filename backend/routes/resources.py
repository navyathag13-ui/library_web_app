"""
/api/resources  — CRUD + checkout/return for resources.

New in final version vs ResourceHub:
  - GET /api/resources/:id          → single resource with full loan history
  - PUT /api/resources/:id          → edit title/author/category/description/isbn/copies
  - POST /api/resources/:id/checkout → creates a Loan (borrower + due date)
  - PATCH /api/resources/:id/return  → closes the oldest active loan for this resource
  - Pagination: page + per_page query params
  - Sorting:    sort_by + sort_order query params
"""
from datetime import datetime, timedelta
from flask import Blueprint, jsonify, request
from models import db, Resource, Loan

resources_bp = Blueprint("resources", __name__, url_prefix="/api")

LOAN_DURATION_DAYS = 14   # default checkout period


def _err(msg: str, code: int):
    return jsonify({"error": msg}), code


# ── GET /api/resources ─────────────────────────────────────────────────────────

@resources_bp.get("/resources")
def list_resources():
    query = Resource.query

    # Search
    search = request.args.get("search", "").strip()
    if search:
        like = f"%{search}%"
        query = query.filter(
            db.or_(Resource.title.ilike(like), Resource.author.ilike(like), Resource.isbn.ilike(like))
        )

    # Filter
    status   = request.args.get("status", "").strip()
    category = request.args.get("category", "").strip()
    if status == "available":
        query = query.filter(Resource.available_copies > 0)
    elif status == "checked-out":
        query = query.filter(Resource.available_copies == 0)
    if category:
        query = query.filter(Resource.category.ilike(f"%{category}%"))

    # Sort
    sort_map = {
        "title":           Resource.title,
        "author":          Resource.author,
        "category":        Resource.category,
        "dateAdded":       Resource.date_added,
        "availableCopies": Resource.available_copies,
    }
    sort_col   = sort_map.get(request.args.get("sort_by", "dateAdded"), Resource.date_added)
    sort_order = request.args.get("sort_order", "desc")
    query = query.order_by(sort_col.desc() if sort_order == "desc" else sort_col.asc())

    # Pagination
    total    = query.count()
    page     = max(1, int(request.args.get("page", 1)))
    per_page = min(100, max(1, int(request.args.get("per_page", 20))))
    resources = query.offset((page - 1) * per_page).limit(per_page).all()

    return jsonify({
        "resources": [r.to_dict() for r in resources],
        "total":     total,
        "page":      page,
        "perPage":   per_page,
        "pages":     max(1, -(-total // per_page)),  # ceiling division
    }), 200


# ── GET /api/resources/:id ─────────────────────────────────────────────────────

@resources_bp.get("/resources/<int:rid>")
def get_resource(rid: int):
    resource = db.get_or_404(Resource, rid)
    return jsonify(resource.to_dict(include_loans=True)), 200


# ── POST /api/resources ────────────────────────────────────────────────────────

@resources_bp.post("/resources")
def create_resource():
    data         = request.get_json(silent=True) or {}
    title        = (data.get("title")        or "").strip()
    author       = (data.get("author")       or "").strip()
    category     = (data.get("category")     or "General").strip()
    description  = (data.get("description")  or "").strip() or None
    isbn         = (data.get("isbn")         or "").strip() or None
    total_copies = int(data.get("totalCopies", 1))

    if not title:  return _err("Title is required", 400)
    if not author: return _err("Author is required", 400)
    if total_copies < 1: return _err("Must have at least 1 copy", 400)

    # Duplicate guard (same title + author, or same ISBN)
    if Resource.query.filter(Resource.title.ilike(title), Resource.author.ilike(author)).first():
        return _err(f"'{title}' by {author} already exists", 409)
    if isbn and Resource.query.filter_by(isbn=isbn).first():
        return _err(f"ISBN {isbn} is already assigned to another resource", 409)

    resource = Resource(
        title=title, author=author, category=category,
        description=description, isbn=isbn,
        total_copies=total_copies, available_copies=total_copies,
    )
    db.session.add(resource)
    db.session.commit()
    return jsonify({"message": f"'{title}' added successfully", "resource": resource.to_dict()}), 201


# ── PUT /api/resources/:id ─────────────────────────────────────────────────────

@resources_bp.put("/resources/<int:rid>")
def update_resource(rid: int):
    resource = db.get_or_404(Resource, rid)
    data     = request.get_json(silent=True) or {}

    title        = (data.get("title")        or "").strip() or resource.title
    author       = (data.get("author")       or "").strip() or resource.author
    category     = (data.get("category")     or "").strip() or resource.category
    description  = data.get("description", resource.description)
    isbn         = (data.get("isbn")         or "").strip() or None

    new_total = int(data.get("totalCopies", resource.total_copies))
    if new_total < 1: return _err("Must have at least 1 copy", 400)

    # Check ISBN uniqueness (exclude self)
    if isbn and isbn != resource.isbn:
        clash = Resource.query.filter_by(isbn=isbn).first()
        if clash and clash.id != rid:
            return _err(f"ISBN {isbn} already assigned to another resource", 409)

    # Adjust available copies proportionally if total changed
    delta = new_total - resource.total_copies
    new_available = max(0, resource.available_copies + delta)

    resource.title            = title
    resource.author           = author
    resource.category         = category
    resource.description      = description or None
    resource.isbn             = isbn
    resource.total_copies     = new_total
    resource.available_copies = new_available
    resource.updated_at       = datetime.utcnow()

    db.session.commit()
    return jsonify({"message": f"'{title}' updated", "resource": resource.to_dict()}), 200


# ── DELETE /api/resources/:id ──────────────────────────────────────────────────

@resources_bp.delete("/resources/<int:rid>")
def delete_resource(rid: int):
    resource = db.get_or_404(Resource, rid)
    if resource.available_copies < resource.total_copies:
        return _err(f"'{resource.title}' has copies currently checked out and cannot be removed", 409)
    title = resource.title
    db.session.delete(resource)
    db.session.commit()
    return jsonify({"message": f"'{title}' removed from the system"}), 200


# ── POST /api/resources/:id/checkout ──────────────────────────────────────────

@resources_bp.post("/resources/<int:rid>/checkout")
def checkout_resource(rid: int):
    resource = db.get_or_404(Resource, rid)
    if resource.available_copies < 1:
        return _err(f"No copies of '{resource.title}' are currently available", 409)

    data          = request.get_json(silent=True) or {}
    borrower_name = (data.get("borrowerName") or "").strip()
    if not borrower_name:
        return _err("Borrower name is required", 400)

    # Due date: caller may pass an ISO string; fall back to default
    due_str = data.get("dueDate", "")
    try:
        due_date = datetime.fromisoformat(due_str) if due_str else None
    except ValueError:
        due_date = None
    if not due_date:
        due_date = datetime.utcnow() + timedelta(days=LOAN_DURATION_DAYS)

    loan = Loan(
        resource_id=rid,
        borrower_name=borrower_name,
        checkout_date=datetime.utcnow(),
        due_date=due_date,
        status="active",
    )
    resource.available_copies -= 1

    db.session.add(loan)
    db.session.commit()
    return jsonify({
        "message":  f"'{resource.title}' checked out to {borrower_name}",
        "loan":     loan.to_dict(),
        "resource": resource.to_dict(),
    }), 201


# ── PATCH /api/resources/:id/return ───────────────────────────────────────────

@resources_bp.patch("/resources/<int:rid>/return")
def return_resource(rid: int):
    resource = db.get_or_404(Resource, rid)
    data     = request.get_json(silent=True) or {}

    # If caller specifies a loan ID use it; otherwise return the oldest active loan
    loan_id = data.get("loanId")
    if loan_id:
        loan = Loan.query.filter_by(id=loan_id, resource_id=rid).first()
    else:
        loan = (Loan.query
                .filter(Loan.resource_id == rid, Loan.status.in_(["active", "overdue"]))
                .order_by(Loan.checkout_date.asc())
                .first())

    if not loan:
        return _err(f"No active loan found for '{resource.title}'", 409)

    now             = datetime.utcnow()
    loan.return_date = now
    loan.status      = "returned"
    resource.available_copies = min(resource.total_copies, resource.available_copies + 1)
    resource.updated_at = now

    db.session.commit()
    return jsonify({
        "message":  f"'{resource.title}' returned by {loan.borrower_name}",
        "loan":     loan.to_dict(),
        "resource": resource.to_dict(),
    }), 200
