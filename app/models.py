from datetime import datetime, timedelta
from flask_login import UserMixin
from app.extensions import db, login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(20), default='user') # 'user' or 'admin'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    orders = db.relationship('Order', backref='customer', lazy=True)
    cart_items = db.relationship('Cart', backref='user', lazy=True)
    reviews = db.relationship('Review', backref='author', lazy=True)
    wishlist_items = db.relationship('Wishlist', backref='user', lazy=True)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    category = db.Column(db.String(64), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text)
    stock = db.Column(db.Integer, default=0)
    rating = db.Column(db.Float, default=0.0)
    image_url = db.Column(db.String(256))
    is_fast_delivery = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    reviews = db.relationship('Review', backref='product', lazy=True)
    cart_added = db.relationship('Cart', backref='product', lazy=True)
    wishlist_added = db.relationship('Wishlist', backref='product', lazy=True)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='Pending') # Pending, Shipped, Delivered
    payment_mode = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    estimated_delivery = db.Column(db.DateTime)
    
    items = db.relationship('OrderItem', backref='order', lazy=True)
    
    @property
    def is_cancelable(self):
        # Order can be cancelled within 2 hours of placement if it's still 'Confirmed' or 'Pending'
        if self.status not in ['Confirmed', 'Pending']:
            return False
        return datetime.utcnow() < self.created_at + timedelta(hours=2)

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    # Store price at time of purchase? For now simplify.
    
    product = db.relationship('Product')

# Transaction log for Apriori (as requested)
class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    quantity = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    
    # product relationship already defined in Product.cart_added via backref or we can define here
    # Since I defined backref in Product, 'product' attribute on Cart object is available if I didn't name it something else.
    # Actually in Product I used backcheck='product'. Wait.
    # In Product: cart_added = db.relationship('Cart', backref='product', lazy=True)
    # This means Cart.product returns variable.

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Wishlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
