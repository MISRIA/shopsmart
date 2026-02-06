import compat
from app import create_app, db
from app.models import User

app = create_app()

def check_users():
    with app.app_context():
        users = User.query.all()
        print("Existing Users:")
        for u in users:
            print(f"ID: {u.id}, Email: {u.email}, Role: {u.role}")

if __name__ == "__main__":
    check_users()
