from flask import Flask
from config import Config
from app.extensions import db, migrate, login_manager, bcrypt


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # -------------------------
    # Initialize Flask extensions
    # -------------------------
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    # -------------------------
    # Register Blueprints
    # -------------------------
    from app.routes.main import main_bp
    from app.routes.auth import auth_bp
    from app.routes.admin import admin_bp
    from app.routes.api import api_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(api_bp, url_prefix="/api")

    # -------------------------
    # Create DB + Auto-seed safely
    # -------------------------
    with app.app_context():
        db.create_all()

        from app.models import Product
        if Product.query.count() == 0:
            try:
                from seed import seed_products
                seed_products()
                print("✅ Database auto-seeded successfully.")
            except Exception as e:
                print("❌ Auto-seeding failed:", e)

    return app
