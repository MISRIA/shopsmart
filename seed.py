import compat
from app import create_app, db
from app.models import Product, User, Review
from datetime import datetime, timedelta
import random

app = create_app()

def seed_products():
    with app.app_context():
        Review.query.delete()
        Product.query.delete()
        
        demo_user = User.query.filter_by(email='user@example.com').first()
        if not demo_user:
            demo_user = User(name="John Doe", email="user@example.com")
            db.session.add(demo_user)
            db.session.flush()

        products_data = [
            # ELECTRONICS
            {
                "name": "Sony WH-1000XM5 Headphones",
                "category": "Electronics",
                "price": 348.00,
                "description": "Premium noise-canceling wireless headphones with industry-leading sound.",
                "stock": 45, "rating": 4.9, "is_fast_delivery": True,
                "image_url": "/static/img/sony_headphones.png"
            },
            {
                "name": "Apple MacBook Pro 14-inch",
                "category": "Electronics",
                "price": 1999.00,
                "description": "M3 Chip, 16GB Unified Memory, 512GB SSD. Space Gray.",
                "stock": 12, "rating": 5.0, "is_fast_delivery": False,
                "image_url": "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=800&q=80"
            },
            {
                "name": "Logitech MX Master 3S Mouse",
                "category": "Electronics",
                "price": 99.00,
                "description": "Ergonomic wireless mouse for high-performance productivity.",
                "stock": 100, "rating": 4.7, "is_fast_delivery": True,
                "image_url": "https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=800&q=80"
            },
            {
                "name": "Mechanical Gaming Keyboard RGB",
                "category": "Electronics",
                "price": 129.00,
                "description": "Tactile switches with customizable RGB lighting per key.",
                "stock": 50, "rating": 4.6, "is_fast_delivery": True,
                "image_url": "https://images.unsplash.com/photo-1511467687858-23d96c32e4ae?w=800&q=80"
            },
            {
                "name": "Samsung Galaxy S24 Ultra",
                "category": "Electronics",
                "price": 1299.99,
                "description": "Titanium Gray AI smartphone with 200MP camera and S-Pen.",
                "stock": 25, "rating": 4.8, "is_fast_delivery": True,
                "image_url": "https://images.unsplash.com/photo-1610945415295-d9bbf067e59c?w=800&q=80"
            },
            {
                "name": "Premium Smart Watch Pro",
                "category": "Electronics",
                "price": 399.00,
                "description": "Advanced health tracking and always-on display.",
                "stock": 30, "rating": 4.7, "is_fast_delivery": True,
                "image_url": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=800&q=80"
            },
            {
                "name": "Wireless Charging Pad",
                "category": "Electronics",
                "price": 45.00,
                "description": "15W fast charging for all Qi-enabled devices.",
                "stock": 120, "rating": 4.4, "is_fast_delivery": True,
                "image_url": "https://images.unsplash.com/photo-1586810165616-94c631fc2f79?w=800&q=80"
            },

            # FASHION
            {
                "name": "Embroidered Cotton Kurta Top",
                "category": "Fashion",
                "price": 49.00,
                "description": "Premium ethnic wear for casual and festive occasions.",
                "stock": 60, "rating": 4.6, "is_fast_delivery": True,
                "image_url": "https://images.unsplash.com/photo-1583391733956-3750e0ff4e8b?w=800&q=80"
            },
            {
                "name": "Silk Blend Leggings",
                "category": "Fashion",
                "price": 25.00,
                "description": "Comfortable and stylish bottom wear for ethnic tops.",
                "stock": 100, "rating": 4.4, "is_fast_delivery": True,
                "image_url": "https://images.unsplash.com/photo-1631541909061-71e349d1f203?w=800&q=80"
            },
            {
                "name": "Lightweight Running Sneakers",
                "category": "Fashion",
                "price": 89.00,
                "description": "Breathable mesh upper with superior cushioning.",
                "stock": 75, "rating": 4.8, "is_fast_delivery": True,
                "image_url": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=800&q=80"
            },
            {
                "name": "Classic Denim Jacket",
                "category": "Fashion",
                "price": 79.99,
                "description": "Vintage washed durable denim for an effortless look.",
                "stock": 40, "rating": 4.5, "is_fast_delivery": False,
                "image_url": "https://images.unsplash.com/photo-1576995853123-5a10305d93c0?w=800&q=80"
            },
            {
                "name": "Aviator Sunglasses",
                "category": "Fashion",
                "price": 120.00,
                "description": "UV protected polarized lenses with gold frame.",
                "stock": 35, "rating": 4.7, "is_fast_delivery": True,
                "image_url": "https://images.unsplash.com/photo-1572635196237-14b3f281503f?w=800&q=80"
            },
            {
                "name": "Traditional Silk Saree",
                "category": "Fashion",
                "price": 150.00,
                "description": "Exquisite hand-woven silk with gold zari border.",
                "stock": 20, "rating": 4.9, "is_fast_delivery": False,
                "image_url": "https://images.unsplash.com/photo-1610030469983-98e550d6193c?w=800&q=80"
            },
            {
                "name": "Slim Fit Formal Shirt",
                "category": "Fashion",
                "price": 45.00,
                "description": "Premium cotton blend for a sharp professional look.",
                "stock": 80, "rating": 4.4, "is_fast_delivery": True,
                "image_url": "https://images.unsplash.com/photo-1617114919297-3c8ddb01f599?w=800&q=80"
            },

            # TOYS
            {
                "name": "LEGO Star Wars Millennium Falcon",
                "category": "Toys",
                "price": 169.99,
                "description": "Detailed LEGO starship with 1,351 pieces.",
                "stock": 15, "rating": 4.9, "is_fast_delivery": False,
                "image_url": "https://images.unsplash.com/photo-1585366119957-e9730b6d0f60?w=800&q=80"
            },
            {
                "name": "Nintendo Switch OLED Model",
                "category": "Toys",
                "price": 349.99,
                "description": "Vibrant 7-inch OLED screen gaming handheld.",
                "stock": 20, "rating": 4.8, "is_fast_delivery": True,
                "image_url": "https://images.unsplash.com/photo-1578303512597-81e6cc155b3e?w=800&q=80"
            },
            {
                "name": "4K Camera Quadcopter Drone",
                "category": "Toys",
                "price": 199.00,
                "description": "GPS assisted flight with 30 mins battery life.",
                "stock": 10, "rating": 4.6, "is_fast_delivery": False,
                "image_url": "https://images.unsplash.com/photo-1507582020474-9a35b7d455d9?w=800&q=80"
            },
            {
                "name": "Junior Chemist Science Kit",
                "category": "Toys",
                "price": 39.99,
                "description": "50+ safe experiments for curious young minds.",
                "stock": 60, "rating": 4.7, "is_fast_delivery": True,
                "image_url": "https://images.unsplash.com/photo-1530210124550-912dc1381cb8?w=800&q=80"
            },
            {
                "name": "Remote Controlled Racing Car",
                "category": "Toys",
                "price": 55.00,
                "description": "High-speed drift car with rechargeable batteries.",
                "stock": 40, "rating": 4.3, "is_fast_delivery": True,
                "image_url": "https://images.unsplash.com/photo-1594731802114-257567690076?w=800&q=80"
            },
            {
                "name": "Eco-Friendly Building Blocks",
                "category": "Toys",
                "price": 29.99,
                "description": "Safe wooden blocks for early development and creativity.",
                "stock": 100, "rating": 4.9, "is_fast_delivery": True,
                "image_url": "https://images.unsplash.com/photo-1587654780291-39c9404d746b?w=800&q=80"
            },
            {
                "name": "Plush Bear Classic",
                "category": "Toys",
                "price": 19.99,
                "description": "Ultra-soft huggable teddy bear for all ages.",
                "stock": 200, "rating": 4.8, "is_fast_delivery": True,
                "image_url": "https://images.unsplash.com/photo-1559454403-b8fb88521f77?w=800&q=80"
            }
        ]
        
        sample_reviews = ["Truly impressive!", "Excellent build quality.", "Worth every penny.", "Super fast delivery!", "Best buy of the year."]

        for p_data in products_data:
            p = Product(**p_data)
            db.session.add(p)
            db.session.flush()
            for _ in range(random.randint(2, 5)):
                db.session.add(Review(user_id=demo_user.id, product_id=p.id, rating=random.randint(4, 5), comment=random.choice(sample_reviews)))
            
        db.session.commit()
        print("Database re-seeded with cross-sell accessories.")

if __name__ == '__main__':
    seed_products()
