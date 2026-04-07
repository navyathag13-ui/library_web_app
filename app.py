"""
LibraryHub — Library Management Web App
A beginner-friendly Flask web application for managing library books.

Run with:
    python app.py
Then open: http://127.0.0.1:5000
"""

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import date

# ── App setup ────────────────────────────────────────────────────────────────
app = Flask(__name__)
app.secret_key = "libraryhub-secret-key"          # needed for flash messages
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///library.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# ── Database model ────────────────────────────────────────────────────────────
class Book(db.Model):
    """Represents a single book in the library."""
    id          = db.Column(db.Integer, primary_key=True)
    title       = db.Column(db.String(300), nullable=False)
    author      = db.Column(db.String(200), nullable=False)
    genre       = db.Column(db.String(100), default="General")
    status      = db.Column(db.String(20), default="available")   # 'available' or 'borrowed'
    borrow_date = db.Column(db.String(20), nullable=True)
    return_date = db.Column(db.String(20), nullable=True)
    date_added  = db.Column(db.String(20), default=str(date.today()))

    def __repr__(self):
        return f"<Book {self.id}: {self.title}>"


# Create all tables when the app starts
with app.app_context():
    db.create_all()


# ── Routes ────────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    """Home page — shows all books, with optional search."""
    search = request.args.get("search", "").strip()
    filter_status = request.args.get("status", "all")

    query = Book.query

    # Search by title or author
    if search:
        query = query.filter(
            db.or_(
                Book.title.ilike(f"%{search}%"),
                Book.author.ilike(f"%{search}%"),
                Book.genre.ilike(f"%{search}%"),
            )
        )

    # Filter by status
    if filter_status in ("available", "borrowed"):
        query = query.filter(Book.status == filter_status)

    books = query.order_by(Book.date_added.desc()).all()

    total      = Book.query.count()
    available  = Book.query.filter_by(status="available").count()
    borrowed   = Book.query.filter_by(status="borrowed").count()

    return render_template(
        "index.html",
        books=books,
        search=search,
        filter_status=filter_status,
        total=total,
        available=available,
        borrowed=borrowed,
    )


@app.route("/add", methods=["GET", "POST"])
def add_book():
    """Show the add-book form (GET) and handle form submission (POST)."""
    if request.method == "POST":
        title  = request.form.get("title", "").strip()
        author = request.form.get("author", "").strip()
        genre  = request.form.get("genre", "General").strip()

        # Validation
        if not title:
            flash("Book title cannot be empty.", "error")
            return render_template("add_book.html")

        if not author:
            flash("Author name cannot be empty.", "error")
            return render_template("add_book.html")

        # Check for duplicate title + author combination
        existing = Book.query.filter(
            Book.title.ilike(title),
            Book.author.ilike(author)
        ).first()
        if existing:
            flash(f'"{title}" by {author} is already in the library.', "error")
            return render_template("add_book.html")

        new_book = Book(title=title, author=author, genre=genre or "General")
        db.session.add(new_book)
        db.session.commit()

        flash(f'"{title}" was added successfully!', "success")
        return redirect(url_for("index"))

    return render_template("add_book.html")


@app.route("/borrow/<int:book_id>", methods=["POST"])
def borrow_book(book_id):
    """Mark a book as borrowed."""
    book = Book.query.get_or_404(book_id)

    if book.status == "borrowed":
        flash(f'"{book.title}" is already borrowed.', "error")
        return redirect(url_for("index"))

    book.status      = "borrowed"
    book.borrow_date = str(date.today())
    book.return_date = None
    db.session.commit()

    flash(f'"{book.title}" has been borrowed.', "success")
    return redirect(url_for("index"))


@app.route("/return/<int:book_id>", methods=["POST"])
def return_book(book_id):
    """Mark a borrowed book as returned (available again)."""
    book = Book.query.get_or_404(book_id)

    if book.status == "available":
        flash(f'"{book.title}" is already available — it was not borrowed.', "error")
        return redirect(url_for("index"))

    book.status      = "available"
    book.return_date = str(date.today())
    db.session.commit()

    flash(f'"{book.title}" has been returned successfully.', "success")
    return redirect(url_for("index"))


@app.route("/delete/<int:book_id>", methods=["POST"])
def delete_book(book_id):
    """Remove a book from the library (only if it is not currently borrowed)."""
    book = Book.query.get_or_404(book_id)

    if book.status == "borrowed":
        flash(f'Cannot remove "{book.title}" — it is currently borrowed.', "error")
        return redirect(url_for("index"))

    db.session.delete(book)
    db.session.commit()

    flash(f'"{book.title}" has been removed from the library.', "success")
    return redirect(url_for("index"))


# ── Run ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app.run(debug=True)
