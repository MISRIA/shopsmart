import compat
from app import create_app, db
from app.models import Product

app = create_app()

def list_categories():
    with app.app_context():
        categories = db.session.query(Product.category).distinct().all()
        print("Unique categories in DB:")
        for cat in categories:
            print(f"- {cat[0]}")

if __name__ == "__main__":
    list_categories()
