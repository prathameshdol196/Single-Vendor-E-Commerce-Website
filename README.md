# Single-Vendor-E-Commerce-Website
# Single Vendor E-commerce Platform

## Description
A single vendor e-commerce platform built with Flask, Bootstrap, and SQLAlchemy. Features include user authentication, product management, shopping cart, and payment integration.

## Features
- User Registration and Login
- Product Listing and Detail Pages
- Shopping Cart Functionality
- Admin Dashboard for Product Management
- Payment Integration with Stripe

## Technologies Used
- Flask
- Bootstrap
- SQLAlchemy
- Stripe

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/ecommerce_app.git
    ```
2. Navigate to the project directory:
    ```bash
    cd ecommerce_app
    ```
3. Create and activate a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
4. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
5. Set environment variables:
    ```bash
    export SECRET_KEY='your_secret_key'
    export STRIPE_PUBLIC_KEY='your_stripe_public_key'
    export STRIPE_SECRET_KEY='your_stripe_secret_key'
    ```
6. Initialize the database:
    ```bash
    flask db init
    flask db migrate
    flask db upgrade
    ```
7. Run the application:
    ```bash
    flask run
    ```

## Deployment
Deployed on Heroku: [Your Heroku App URL](https://your-app.herokuapp.com)

## Admin Credentials
- **Username**: admin
- **Password**: adminpassword

## Screenshots
![Home Page](screenshots/home.png)
![Admin Dashboard](screenshots/admin_dashboard.png)
