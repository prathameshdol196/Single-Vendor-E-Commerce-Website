from flask import render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from . import db
from .models import Product, Order, OrderProduct
from .forms import ProductForm
from flask import Blueprint
import os
from werkzeug.utils import secure_filename

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@admin_bp.route("/dashboard")
@login_required
def dashboard():
    if not current_user.is_admin:
        flash('Access denied.', 'danger')
        return redirect(url_for('main.home'))

    page = request.args.get('page', 1, type=int)
    products = Product.query.paginate(page=page, per_page=10)
    orders = Order.query.order_by(Order.date_ordered.desc()).paginate(page=page, per_page=10)

    return render_template('admin/dashboard.html', products=products, orders=orders)


@admin_bp.route("/add_product", methods=["GET", "POST"])
@login_required
def add_product():
    if not current_user.is_admin:
        flash('Access denied.', 'danger')
        return redirect(url_for('main.home'))
    form = ProductForm()
    if form.validate_on_submit():
        try:
            if form.image.data and allowed_file(form.image.data.filename):
                filename = secure_filename(form.image.data.filename)
                images_path = os.path.join(current_app.root_path, 'static', 'images')
                os.makedirs(images_path, exist_ok=True)
                image_path = os.path.join(images_path, filename)

                # Optional: Validate image using Pillow
                # image = Image.open(form.image.data)
                # image.verify()

                form.image.data.save(image_path)
            else:
                filename = 'default.jpg'  # Or handle accordingly

            product = Product(
                name=form.name.data,
                description=form.description.data,
                price=form.price.data,
                stock=form.stock.data,
                image_file=filename
            )
            db.session.add(product)
            db.session.commit()
            flash('Product added successfully!', 'success')
            return redirect(url_for('admin.dashboard'))
        except Exception as e:
            current_app.logger.error(f'Error adding product: {e}')
            flash('An error occurred while adding the product. Please try again.', 'danger')
            return redirect(url_for('admin.add_product'))
    return render_template('admin/add_product.html', form=form)


@admin_bp.route("/edit_product/<int:product_id>", methods=["GET", "POST"])
@login_required
def edit_product(product_id):
    if not current_user.is_admin:
        flash("Access denied.", "danger")
        return redirect(url_for("main.home"))
    product = Product.query.get_or_404(product_id)
    form = ProductForm(obj=product)
    if form.validate_on_submit():
        if form.image.data:
            filename = secure_filename(form.image.data.filename)
            image_path = os.path.join(current_app.root_path, "static/images", filename)
            form.image.data.save(image_path)
            product.image_file = filename
        product.name = form.name.data
        product.description = form.description.data
        product.price = form.price.data
        product.stock = form.stock.data
        db.session.commit()
        flash("Product updated successfully!", "success")
        return redirect(url_for("admin.dashboard"))
    return render_template("admin/edit_product.html", form=form, product=product)


@admin_bp.route("/delete_product/<int:product_id>", methods=["POST"])
@login_required
def delete_product(product_id):
    if not current_user.is_admin:
        flash("Access denied.", "danger")
        return redirect(url_for("main.home"))
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash("Product deleted successfully!", "success")
    return redirect(url_for("admin.dashboard"))
