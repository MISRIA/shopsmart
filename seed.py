from app.extensions import db
from app.models import Product, User, Review
import random


def seed_products():
    """
    This function assumes it is already running inside app.app_context()
    DO NOT create the app here.
    """

    # Clear existing data
    Review.query.delete()
    Product.query.delete()

    # Create demo user
    demo_user = User.query.filter_by(email="user@example.com").first()
    if not demo_user:
        demo_user = User(name="John Doe", email="user@example.com")
        db.session.add(demo_user)
        db.session.flush()

    products_data = [

        # ================= ELECTRONICS =================
        {
            "name": "Sony WH-1000XM5 Headphones",
            "category": "Electronics",
            "price": 348.00,
            "description": "Industry-leading noise cancelling headphones.",
            "stock": 40,
            "rating": 4.9,
            "is_fast_delivery": True,
            "image_url": "https://images.unsplash.com/photo-1518441902112-f4e8a9b5b52c"
        },
        {
            "name": "Apple iPhone 15 Pro",
            "category": "Electronics",
            "price": 1199.00,
            "description": "Titanium body, A17 Pro chip.",
            "stock": 25,
            "rating": 4.8,
            "is_fast_delivery": True,
            "image_url": "https://images.unsplash.com/photo-1695048133142-1a20484d256c"
        },
        {
            "name": "Logitech MX Master 3S Mouse",
            "category": "Electronics",
            "price": 99.00,
            "description": "Ergonomic productivity mouse.",
            "stock": 80,
            "rating": 4.7,
            "is_fast_delivery": True,
            "image_url": "https://images.unsplash.com/photo-1587829741301-dc798b83add3"
        },

        # ================= FASHION =================
        {
            "name": "Men Slim Fit Formal Shirt",
            "category": "Fashion",
            "price": 39.99,
            "description": "Premium cotton formal wear.",
            "stock": 100,
            "rating": 4.5,
            "is_fast_delivery": True,
            "image_url": "https://images.unsplash.com/photo-1603252109303-2751441dd157"
        },
        {
            "name": "Women Summer Kurti",
            "category": "Fashion",
            "price": 29.99,
            "description": "Lightweight ethnic kurti.",
            "stock": 70,
            "rating": 4.6,
            "is_fast_delivery": True,
            "image_url": "https://images.unsplash.com/photo-1583391733956-3750e0ff4e8b"
        },
        {
            "name": "Running Sneakers",
            "category": "Fashion",
            "price": 79.00,
            "description": "Breathable sports shoes.",
            "stock": 60,
            "rating": 4.8,
            "is_fast_delivery": True,
            "image_url": "https://images.unsplash.com/photo-1542291026-7eec264c27ff"
        },

        # ================= TOYS =================
        {
            "name": "LEGO City Police Set",
            "category": "Toys",
            "price": 89.99,
            "description": "Creative building blocks for kids.",
            "stock": 50,
            "rating": 4.9,
            "is_fast_delivery": False,
            "image_url": "https://images.unsplash.com/photo-1585366119957-e9730b6d0f60"
        },
        {
            "name": "Remote Control Racing Car",
            "category": "Toys",
            "price": 49.99,
            "description": "High-speed RC car.",
            "stock": 90,
            "rating": 4.4,
            "is_fast_delivery": True,
            "image_url": "https://images.unsplash.com/photo-1594731802114-257567690076"
        },

        # ================= HOME & KITCHEN =================
        {
            "name": "Non-Stick Cookware Set",
            "category": "Home & Kitchen",
            "price": 129.00,
            "description": "Durable non-stick cooking set.",
            "stock": 45,
            "rating": 4.6,
            "is_fast_delivery": True,
            "image_url": "https://images.unsplash.com/photo-1586201375754-1421e3f8d6c1"
        },
        {
            "name": "Electric Kettle",
            "category": "Home & Kitchen",
            "price": 35.00,
            "description": "Fast boiling stainless steel kettle.",
            "stock": 120,
            "rating": 4.5,
            "is_fast_delivery": True,
            "image_url": "https://images.unsplash.com/photo-1606813909024-57a16b2c8b6f"
        },

        # ================= BEAUTY =================
        {
            "name": "Vitamin C Face Serum",
            "category": "Beauty",
            "price": 24.99,
            "description": "Brightening skin serum.",
            "stock": 150,
            "rating": 4.7,
            "is_fast_delivery": True,
            "image_url": "https://images.unsplash.com/photo-1611930022073-b7a4ba5fcccd"
        },
        {
            "name": "Herbal Shampoo",
            "category": "Beauty",
            "price": 14.99,
            "description": "Natural hair care solution.",
            "stock": 200,
            "rating": 4.4,
            "is_fast_delivery": True,
            "image_url": "https://images.unsplash.com/photo-1596462502278-27bfdc403348"
        },

        # ================= BOOKS =================
        {
            "name": "Atomic Habits",
            "category": "Books",
            "price": 19.99,
            "description": "Bestselling self-improvement book.",
            "stock": 300,
            "rating": 4.9,
            "is_fast_delivery": True,
            "image_url": "https://images.unsplash.com/photo-1544947950-fa07a98d237f"
        },
        {
            "name": "Python Programming Guide",
            "category": "Books",
            "price": 29.99,
            "description": "Beginner to advanced Python concepts.",
            "stock": 180,
            "rating": 4.8,
            "is_fast_delivery": True,
            "image_url": "https://images.unsplash.com/photo-1512820790803-83ca734da794"
        }
    ]

    sample_reviews = [
        "Truly impressive!",
        "Excellent build quality.",
        "Worth every penny.",
        "Super fast delivery!",
        "Best buy of the year."
    ]

    for p_data in products_data:
        product = Product(**p_data)
        db.session.add(product)
        db.session.flush()

        for _ in range(random.randint(2, 5)):
            db.session.add(
                Review(
                    user_id=demo_user.id,
                    product_id=product.id,
                    rating=random.randint(4, 5),
                    comment=random.choice(sample_reviews)
                )
            )

    db.session.commit()
    print("✅ Products seeded successfully.")
