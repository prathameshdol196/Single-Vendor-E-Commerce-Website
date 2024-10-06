from flask import render_template, redirect, url_for, flash, request, session
from flask_login import login_user, current_user, logout_user, login_required
from . import db
from .models import User, Product, Order, OrderProduct
from .forms import RegistrationForm, LoginForm
from flask import Blueprint

# Define Blueprint
main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def home():
    products = Product.query.all()
    return render_template('index.html', products=products)


@main_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)


@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash('Logged in successfully!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password.', 'danger')
    return render_template('login.html', form=form)


@main_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@main_bp.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product.html', product=product)


@main_bp.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)
    cart = session.get('cart', {})
    if str(product_id) in cart:
        cart[str(product_id)] += 1
    else:
        cart[str(product_id)] = 1
    session['cart'] = cart
    flash(f'Added {product.name} to cart.', 'success')
    return redirect(url_for('main.home'))


@main_bp.route('/cart')
def cart():
    cart = session.get('cart', {})
    products = []
    total = 0
    for product_id, quantity in cart.items():
        product = Product.query.get(int(product_id))
        if product:
            products.append({
                'product': product,
                'quantity': quantity,
                'subtotal': product.price * quantity
            })
            total += product.price * quantity
    return render_template('cart.html', products=products, total=total)


@main_bp.route('/remove_from_cart/<int:product_id>', methods=['POST'])
def remove_from_cart(product_id):
    cart = session.get('cart', {})
    if str(product_id) in cart:
        del cart[str(product_id)]
        session['cart'] = cart
        flash('Item removed from cart.', 'success')
    return redirect(url_for('main.cart'))


@main_bp.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    cart = session.get('cart', {})
    if not cart:
        flash('Your cart is empty.', 'warning')
        return redirect(url_for('main.home'))
    if request.method == 'POST':
        # Process order
        total = 0
        order = Order(user_id=current_user.id, total=0)
        db.session.add(order)
        db.session.commit()
        for product_id, quantity in cart.items():
            product = Product.query.get(int(product_id))
            if product and product.stock >= quantity:
                order_product = OrderProduct(order_id=order.id, product_id=product.id, quantity=quantity)
                db.session.add(order_product)
                product.stock -= quantity
                total += product.price * quantity
            else:
                flash('One or more products are out of stock.', 'danger')
                return redirect(url_for('main.cart'))
        order.total = total
        db.session.commit()
        session['cart'] = {}
        flash('Order placed successfully!', 'success')
        return redirect(url_for('main.home'))
    return render_template('checkout.html')
