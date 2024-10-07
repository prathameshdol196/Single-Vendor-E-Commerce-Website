from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, FloatField, IntegerField, \
    FileField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from .models import User


class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=2, max=150)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Username already exists. Please choose another.")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("Email already registered. Please choose another.")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")


class ProductForm(FlaskForm):
    name = StringField("Product Name", validators=[DataRequired(), Length(min=2, max=150)])
    description = TextAreaField("Description", validators=[DataRequired()])
    price = FloatField("Price", validators=[DataRequired()])
    stock = IntegerField("Stock Quantity", validators=[DataRequired()])
    image = FileField("Product Image")
    submit = SubmitField("Submit")
