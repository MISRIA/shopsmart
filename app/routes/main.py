from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from datetime import datetime, timedelta
from app.extensions import db
from app.models import Product, Cart, Order, OrderItem, Transaction, Wishlist, Review
from app.services.recommendation import get_recommendations

main_bp = Blueprint('main', __name__)

@main_bp.context_processor
def inject_cart_count():
    if current_user.is_authenticated:
        items = Cart.query.filter_by(user_id=current_user.id).all()
        count = sum(item.quantity for item in items)
        return {'cart_item_count': count}
    return {'cart_item_count': 0}

@main_bp.route('/')
def home():
    featured_products = Product.query.limit(4).all()
    # Logic to fetch diverse categories
    electronics = Product.query.filter_by(category='Electronics').limit(4).all()
    fashion = Product.query.filter_by(category='Fashion').limit(4).all()
    toys = Product.query.filter_by(category='Toys').limit(4).all()
    
    return render_template('index.html', 
                           featured_products=featured_products, 
                           electronics=electronics,
                           fashion=fashion,
                           toys=toys)

@main_bp.route('/products')
def products():
    page = request.args.get('page', 1, type=int)
    category = request.args.get('category')
    sort = request.args.get('sort')
    query_str = request.args.get('q')
    
    query = Product.query
    if category and category != 'All':
        query = query.filter_by(category=category)
        
    if query_str:
        query = query.filter(
            (Product.name.ilike(f'%{query_str}%')) | 
            (Product.description.ilike(f'%{query_str}%')) |
            (Product.category.ilike(f'%{query_str}%'))
        )
        
    if sort == 'price_asc':
        query = query.order_by(Product.price.asc())
    elif sort == 'price_desc':
        query = query.order_by(Product.price.desc())
    else:
        query = query.order_by(Product.created_at.desc())
        
    products_pagination = query.paginate(page=page, per_page=12)
    return render_template('products/list.html', 
                           products=products_pagination, 
                           current_category=category,
                           current_sort=sort,
                           query=query_str)

@main_bp.route('/product/<int:id>')
def product_detail(id):
    product = Product.query.get_or_404(id)
    return render_template('products/detail.html', product=product, get_recommendations=get_recommendations)

@main_bp.route('/cart')
@login_required
def cart():
    cart_items = Cart.query.filter_by(user_id=current_user.id).all()
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render_template('cart.html', cart_items=cart_items, total_price=round(total_price, 2))

@main_bp.route('/add_to_cart/<int:id>', methods=['POST'])
@login_required
def add_to_cart(id):
    product = Product.query.get_or_404(id)
    if product.stock <= 0:
        flash('Product out of stock', 'danger')
        return redirect(url_for('main.product_detail', id=id))

    quantity = int(request.form.get('quantity', 1))
    
    cart_item = Cart.query.filter_by(user_id=current_user.id, product_id=id).first()
    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = Cart(user_id=current_user.id, product_id=id, quantity=quantity)
        db.session.add(cart_item)
    
    db.session.commit()
    
    # Buy Now redirect logic
    if request.form.get('buy_now') == 'true':
        return redirect(url_for('main.checkout'))
        
    flash(f'Added {product.name} to cart', 'success')
    return redirect(url_for('main.cart'))

@main_bp.route('/cart/update/<int:id>', methods=['POST'])
@login_required
def update_cart(id):
    cart_item = Cart.query.get_or_404(id)
    if cart_item.user_id != current_user.id:
        abort(403)
    
    quantity = int(request.form.get('quantity'))
    if quantity > 0:
        cart_item.quantity = quantity
        db.session.commit()
    return redirect(url_for('main.cart'))

@main_bp.route('/cart/remove/<int:id>')
@login_required
def remove_from_cart(id):
    cart_item = Cart.query.get_or_404(id)
    if cart_item.user_id != current_user.id:
        abort(403)
        
    db.session.delete(cart_item)
    db.session.commit()
    flash('Item removed from cart', 'info')
    return redirect(url_for('main.cart'))

@main_bp.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    cart_items = Cart.query.filter_by(user_id=current_user.id).all()
    if not cart_items:
        return redirect(url_for('main.products'))
        
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    
    if request.method == 'POST':
        # Create Order
        new_order = Order(
            user_id=current_user.id, 
            total_price=total_price, 
            payment_mode=request.form.get('payment_method'), 
            status='Confirmed',
            estimated_delivery=datetime.utcnow() + timedelta(days=5)
        )
        db.session.add(new_order)
        db.session.flush() # Get ID
        
        # Move cart to order items and Transaction log
        is_order_fast = True
        for item in cart_items:
            # Check if all items are fast delivery
            if not item.product.is_fast_delivery:
                is_order_fast = False
                
            order_item = OrderItem(order_id=new_order.id, product_id=item.product.id, quantity=item.quantity)
            db.session.add(order_item)
            
            # Log for AI
            transaction = Transaction(user_id=current_user.id, product_id=item.product.id, quantity=item.quantity)
            db.session.add(transaction)
            
            # Decrease stock
            item.product.stock -= item.quantity
            
        # Update order delivery date based on items
        if is_order_fast:
            new_order.estimated_delivery = datetime.utcnow() + timedelta(days=1)
        else:
            new_order.estimated_delivery = datetime.utcnow() + timedelta(days=5)
            
        # Clear Cart
        Cart.query.filter_by(user_id=current_user.id).delete()
        db.session.commit()
        flash('Order placed successfully!', 'success')
        return redirect(url_for('main.home'))

    return render_template('checkout.html', cart_items=cart_items, total_price=round(total_price, 2))
        
@main_bp.route('/wishlist')
@login_required
def wishlist():
    wishlist_items = Wishlist.query.filter_by(user_id=current_user.id).all()
    return render_template('wishlist.html', wishlist_items=wishlist_items)

@main_bp.route('/add_to_wishlist/<int:id>')
@login_required
def add_to_wishlist(id):
    existing = Wishlist.query.filter_by(user_id=current_user.id, product_id=id).first()
    if not existing:
        new_item = Wishlist(user_id=current_user.id, product_id=id)
        db.session.add(new_item)
        db.session.commit()
        flash('Added to Wishlist', 'success')
    else:
        flash('Already in Wishlist', 'info')
    return redirect(request.referrer or url_for('main.home'))

@main_bp.route('/wishlist/remove/<int:id>')
@login_required
def remove_from_wishlist(id):
    item = Wishlist.query.get_or_404(id)
    if item.user_id != current_user.id:
        abort(403)
    db.session.delete(item)
    db.session.commit()
    flash('Removed from Wishlist', 'success')
    return redirect(url_for('main.wishlist'))

@main_bp.route('/orders')
@login_required
def orders():
    orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
    return render_template('orders.html', orders=orders)

@main_bp.route('/cancel_order/<int:id>', methods=['POST'])
@login_required
def cancel_order(id):
    order = Order.query.get_or_404(id)
    if order.user_id != current_user.id:
        abort(403)
    
    if not order.is_cancelable:
        flash('Order cannot be cancelled after 2 hours.', 'danger')
        return redirect(url_for('main.orders'))
    
    # Restore stock
    for item in order.items:
        item.product.stock += item.quantity
    
    order.status = 'Cancelled'
    db.session.commit()
    flash('Order cancelled successfully.', 'success')
    return redirect(url_for('main.orders'))

@main_bp.route('/add_review/<int:id>', methods=['POST'])
@login_required
def add_review(id):
    product = Product.query.get_or_404(id)
    rating = int(request.form.get('rating', 5))
    comment = request.form.get('comment', '')
    
    new_review = Review(
        user_id=current_user.id,
        product_id=id,
        rating=rating,
        comment=comment
    )
    db.session.add(new_review)
    
    # Update product average rating
    all_reviews = Review.query.filter_by(product_id=id).all()
    # Include the new review in the average
    total_ratings = sum(r.rating for r in all_reviews) + rating
    count = len(all_reviews) + 1
    product.rating = round(total_ratings / count, 1)
    
    db.session.commit()
    flash('Review submitted successfully!', 'success')
    return redirect(url_for('main.product_detail', id=id))
