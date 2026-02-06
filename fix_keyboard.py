from app import create_app, db
from app.models import Product

app = create_app()
with app.app_context():
    try:
        p = Product.query.filter_by(name='Mechanical Gaming Keyboard RGB').first()
        if p:
            # Use a very common, reliable Unsplash ID
            p.image_url = 'https://images.unsplash.com/photo-1511467687858-23d96c32e4ae?w=600&q=80'
            db.session.commit()
            print(f"SUCCESS: Updated {p.name} image.")
        else:
            print("ERROR: Product not found.")
    except Exception as e:
        print(f"CRITICAL ERROR: {e}")
