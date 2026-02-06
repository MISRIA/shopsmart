import compat
from app import create_app, db
from app.models import Product

app = create_app()

def update_images():
    updates = {
        "Sony WH-1000XM5 Headphones": "/static/img/sony_headphones.png",
        "Apple MacBook Pro 14-inch": "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=800&q=80",
        "Logitech MX Master 3S Mouse": "https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=800&q=80",
        # Add more if needed
    }

    with app.app_context():
        for name, url in updates.items():
            product = Product.query.filter_by(name=name).first()
            if product:
                product.image_url = url
                print(f"Updated image for: {name}")
        
        db.session.commit()
        print("Image updates complete.")

if __name__ == "__main__":
    update_images()
