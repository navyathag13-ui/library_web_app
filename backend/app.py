"""
LibraryHub — Flask REST API entry point.

Run:
    cd backend
    source .venv/bin/activate
    python app.py
"""
from datetime import datetime
from flask import Flask
from flask_cors import CORS
from models import db, Loan
from routes.resources import resources_bp
from routes.loans     import loans_bp
from routes.stats     import stats_bp


def _sync_overdue(app: Flask) -> None:
    """Mark past-due active loans as overdue on startup (from Library_borrowing pattern)."""
    with app.app_context():
        now     = datetime.utcnow()
        updated = (
            db.session.query(Loan)
            .filter(Loan.status == "active", Loan.due_date < now)
            .update({"status": "overdue"})
        )
        db.session.commit()
        if updated:
            print(f"[startup] Marked {updated} loan(s) as overdue")


def create_app() -> Flask:
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"]        = "sqlite:///libraryhub.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"]                     = "dev-secret-replace-in-prod"

    CORS(app, resources={r"/api/*": {"origins": ["http://localhost:5173", "http://localhost:4173"]}})

    db.init_app(app)

    app.register_blueprint(resources_bp)
    app.register_blueprint(loans_bp)
    app.register_blueprint(stats_bp)

    with app.app_context():
        db.create_all()

    _sync_overdue(app)
    return app


if __name__ == "__main__":
    application = create_app()
    application.run(debug=True, port=5000)
