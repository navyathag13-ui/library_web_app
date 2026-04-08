"""
LibraryHub data models.

Merges the best of all three source projects:
  - Resource  : multi-copy book/item (Library_borrowing concepts + ResourceHub naming)
  - Loan      : borrow/return record with borrower name, due date, overdue tracking
                (from Library_borrowing's loan service logic, simplified — no user auth)
"""
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# ── Resource ──────────────────────────────────────────────────────────────────

class Resource(db.Model):
    __tablename__ = "resources"

    id               = db.Column(db.Integer, primary_key=True)
    title            = db.Column(db.String(200), nullable=False)
    author           = db.Column(db.String(200), nullable=False)
    category         = db.Column(db.String(100), nullable=False, default="General")
    description      = db.Column(db.Text,        nullable=True)
    isbn             = db.Column(db.String(20),  nullable=True, unique=True)   # optional
    total_copies     = db.Column(db.Integer,     nullable=False, default=1)
    available_copies = db.Column(db.Integer,     nullable=False, default=1)
    date_added       = db.Column(db.DateTime,    default=datetime.utcnow)
    updated_at       = db.Column(db.DateTime,    default=datetime.utcnow, onupdate=datetime.utcnow)

    loans = db.relationship(
        "Loan",
        backref="resource",
        lazy="dynamic",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    @property
    def status(self) -> str:
        return "available" if self.available_copies > 0 else "checked-out"

    def to_dict(self, include_loans: bool = False) -> dict:
        data = {
            "id":              self.id,
            "title":           self.title,
            "author":          self.author,
            "category":        self.category,
            "description":     self.description,
            "isbn":            self.isbn,
            "totalCopies":     self.total_copies,
            "availableCopies": self.available_copies,
            "status":          self.status,
            "dateAdded":       self.date_added.isoformat()  if self.date_added  else None,
            "updatedAt":       self.updated_at.isoformat()  if self.updated_at  else None,
        }
        if include_loans:
            data["loans"] = [l.to_dict() for l in
                             self.loans.order_by(Loan.checkout_date.desc()).all()]
        return data

    def __repr__(self) -> str:
        return f"<Resource {self.id}: {self.title!r} [{self.available_copies}/{self.total_copies}]>"


# ── Loan ──────────────────────────────────────────────────────────────────────

class Loan(db.Model):
    __tablename__ = "loans"

    id            = db.Column(db.Integer,  primary_key=True)
    resource_id   = db.Column(db.Integer,  db.ForeignKey("resources.id", ondelete="CASCADE"), nullable=False, index=True)
    borrower_name = db.Column(db.String(200), nullable=False)
    checkout_date = db.Column(db.DateTime, default=datetime.utcnow)
    due_date      = db.Column(db.DateTime, nullable=False)
    return_date   = db.Column(db.DateTime, nullable=True)
    status        = db.Column(db.String(20), nullable=False, default="active")
    # status: "active" | "returned" | "overdue"

    @property
    def is_overdue(self) -> bool:
        if self.status == "returned":
            return False
        return datetime.utcnow() > self.due_date

    def to_dict(self) -> dict:
        return {
            "id":            self.id,
            "resourceId":    self.resource_id,
            "resourceTitle": self.resource.title if self.resource else None,
            "borrowerName":  self.borrower_name,
            "checkoutDate":  self.checkout_date.isoformat() if self.checkout_date else None,
            "dueDate":       self.due_date.isoformat()      if self.due_date      else None,
            "returnDate":    self.return_date.isoformat()   if self.return_date   else None,
            "status":        self.status,
            "isOverdue":     self.is_overdue,
        }

    def __repr__(self) -> str:
        return f"<Loan {self.id}: {self.borrower_name!r} → resource {self.resource_id} [{self.status}]>"
