import compat
from app import create_app, db
from app.models import Product, Order, User
from datetime import datetime, timedelta

app = create_app()

def test_search():
    print("--- Testing expanded search ---")
    with app.app_context():
        # Search for "M3" which should be in MacBook description
        query = Product.query.filter(
            (Product.name.ilike('%M3%')) | 
            (Product.description.ilike('%M3%')) |
            (Product.category.ilike('%M3%'))
        ).all()
        
        found = any("MacBook" in p.name for p in query)
        if found:
            print("SUCCESS: Found MacBook using 'M3' search query.")
        else:
            print("FAILURE: Could not find MacBook using 'M3' search query.")

def test_cancellation_logic():
    print("\n--- Testing cancellation logic ---")
    with app.app_context():
        user = User.query.first()
        if not user:
            print("No user found in DB, please seed first.")
            return

        # 1. New order
        now = datetime.utcnow()
        o1 = Order(user_id=user.id, total_price=10.0, status='Confirmed', created_at=now)
        db.session.add(o1)
        db.session.flush()
        print(f"New order (status: {o1.status}, age: 0h) is_cancelable: {o1.is_cancelable}")
        
        # 2. Old order
        three_hours_ago = now - timedelta(hours=3)
        o2 = Order(user_id=user.id, total_price=20.0, status='Confirmed', created_at=three_hours_ago)
        db.session.add(o2)
        db.session.flush()
        print(f"Old order (status: {o2.status}, age: 3h) is_cancelable: {o2.is_cancelable}")
        
        # 3. Shipped order
        o3 = Order(user_id=user.id, total_price=30.0, status='Shipped', created_at=now)
        db.session.add(o3)
        db.session.flush()
        print(f"Shipped order (status: {o3.status}, age: 0h) is_cancelable: {o3.is_cancelable}")
        
        db.session.rollback()

if __name__ == "__main__":
    try:
        test_search()
        test_cancellation_logic()
    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()
