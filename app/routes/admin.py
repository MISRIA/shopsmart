from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app.extensions import db
from app.models import Product, Order, User

admin_bp = Blueprint('admin', __name__)

def check_admin():
    """Helper to ensure user is admin"""
    if not current_user.is_authenticated or current_user.role != 'admin':
        abort(403)

@admin_bp.route('/')
@login_required
def dashboard():
    check_admin()
    product_count = Product.query.count()
    order_count = Order.query.count()
    user_count = User.query.count()
    return render_template('admin/dashboard.html', 
                           product_count=product_count, 
                           order_count=order_count, 
                           user_count=user_count)

@admin_bp.route('/products')
@login_required
def manage_products():
    check_admin()
    products = Product.query.all()
    return render_template('admin/products.html', products=products)

@admin_bp.route('/products/add', methods=['GET', 'POST'])
@login_required
def add_product():
    check_admin()
    if request.method == 'POST':
        name = request.form.get('name')
        category = request.form.get('category')
        price = float(request.form.get('price'))
        description = request.form.get('description')
        stock = int(request.form.get('stock'))
        image_url = request.form.get('image_url')
        
        product = Product(name=name, category=category, price=price, 
                          description=description, stock=stock, image_url=image_url)
        db.session.add(product)
        db.session.commit()
        flash('Product created successfully!', 'success')
        return redirect(url_for('admin.manage_products'))
    return render_template('admin/product_form.html', product=None)

@admin_bp.route('/products/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_product(id):
    check_admin()
    product = Product.query.get_or_404(id)
    if request.method == 'POST':
        product.name = request.form.get('name')
        product.category = request.form.get('category')
        product.price = float(request.form.get('price'))
        product.description = request.form.get('description')
        product.stock = int(request.form.get('stock'))
        product.image_url = request.form.get('image_url')
        
        db.session.commit()
        flash('Product updated successfully!', 'success')
        return redirect(url_for('admin.manage_products'))
    return render_template('admin/product_form.html', product=product)

@admin_bp.route('/products/<int:id>/delete')
@login_required
def delete_product(id):
    check_admin()
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted successfully!', 'success')
    return redirect(url_for('admin.manage_products'))

@admin_bp.route('/orders')
@login_required
def manage_orders():
    check_admin()
    orders = Order.query.order_by(Order.created_at.desc()).all()
    return render_template('admin/orders.html', orders=orders)

@admin_bp.route('/orders/<int:id>/status', methods=['POST'])
@login_required
def update_order_status(id):
    check_admin()
    order = Order.query.get_or_404(id)
    new_status = request.form.get('status')
    if new_status in ['Pending', 'Confirmed', 'Shipped', 'Delivered', 'Cancelled']:
        order.status = new_status
        db.session.commit()
        flash(f'Order #{id} status updated to {new_status}', 'success')
    return redirect(url_for('admin.manage_orders'))

@admin_bp.route('/users')
@login_required
def manage_users():
    check_admin()
    users = User.query.all()
    return render_template('admin/users.html', users=users)

@admin_bp.route('/users/<int:id>/role', methods=['POST'])
@login_required
def change_user_role(id):
    check_admin()
    if id == current_user.id:
        flash('You cannot change your own role!', 'danger')
        return redirect(url_for('admin.manage_users'))
    
    user = User.query.get_or_404(id)
    new_role = 'admin' if user.role == 'user' else 'user'
    user.role = new_role
    db.session.commit()
    flash(f'User {user.email} role updated to {new_role}', 'success')
    return redirect(url_for('admin.manage_users'))
