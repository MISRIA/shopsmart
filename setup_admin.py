import compat
from app import create_app, db, bcrypt
from app.models import User

app = create_app()

def setup_admin():
    with app.app_context():
        admin_email = "admin@shopsmart.com"
        admin_pass = "admin123"
        
        admin = User.query.filter_by(email=admin_email).first()
        if not admin:
            hashed_password = bcrypt.generate_password_hash(admin_pass).decode('utf-8')
            admin = User(
                name="System Admin",
                email=admin_email,
                password_hash=hashed_password,
                role="admin"
            )
            db.session.add(admin)
            db.session.commit()
            print(f"Admin user created. Email: {admin_email}, Password: {admin_pass}")
        else:
            admin.role = "admin"
            db.session.commit()
            print(f"User {admin_email} promoted to admin.")

if __name__ == "__main__":
    setup_admin()
