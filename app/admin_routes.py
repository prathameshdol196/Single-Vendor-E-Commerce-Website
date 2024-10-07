from flask import render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from . import db
from .models import Product, Order, OrderProduct
from .forms import ProductForm
from flask import Blueprint
import os
from werkzeug.utils import secure_filename

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.route("/dashboard")
@login_required
def dashboard():
    if not current_user.is_admin:
        flash("Access denied.", "danger")
        return redirect(url_for("main.home"))
    products = Product.query.all()
    orders = Order.query.order_by(Order.date_ordered.desc()).all()
    return render_template("admin/dashboard.html", products=products, orders=orders)


@admin_bp.route("/add_product", methods=["GET", "POST"])
@login_required
def add_product():
    if not current_user.is_admin:
        flash("Access denied.", "danger")
        return redirect(url_for("main.home"))
    form = ProductForm()
    if form.validate_on_submit():
        filename = "default.jpg"
        if form.image.data:
            filename = secure_filename(form.image.data.filename)
            image_path = os.path.join(current_app.root_path, "static/images", filename)
            form.image.data.save(image_path)
        product = Product(
            name=form.name.data,
            description=form.description.data,
            price=form.price.data,
            stock=form.stock.data,
            image_file=filename
        )
        db.session.add(product)
        db.session.commit()
        flash("Product added successfully!", "success")
        return redirect(url_for("admin.dashboard"))
    return render_template("admin/add_product.html", form=form)


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
