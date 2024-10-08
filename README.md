# Single Vendor E-commerce Website

This project is a fully functional Single Vendor E-commerce Website developed using Flask, PostgreSQL, and hosted on Render. It features a basic product catalog, user authentication, a shopping cart, and an admin dashboard for managing products and customer orders.

## Features
- **Product Listing:** Customers can browse through available products.
- **User Authentication:** Both customers and admins have dedicated login systems.
- **Shopping Cart:** Customers can add products to their cart and proceed to checkout.
- **Admin Dashboard:** The admin can manage products, view customer orders, and update product information.
- **PostgreSQL Integration:** The application uses PostgreSQL as its database, with smooth internal connectivity via Render.
- **Deployment on Render:** The entire application, including the backend, frontend, and database, is deployed using Render, ensuring seamless integration and reliable performance.


## Technologies Used
- **Backend:** Flask (Python)
- **Frontend:** HTML, CSS, Jinja2, Bootstrap
- **Database:** PostgreSQL
- **Hosting:** Render (supports backend, frontend, and database hosting)




## Why Render?
Render was chosen as the hosting platform due to its robust support for deploying full-stack applications, with easy internal connection to PostgreSQL. Having used Render previously, I was familiar with its setup, making the process more efficient and reliable. Its all-in-one platform allows for handling the backend, frontend, and database in a unified way, making the deployment simpler and faster.

## To-do
- **UI Improvements:** The current UI is functional but minimal. Improvements can be made based on specific requirements or preferences. I focused more on the backend functionality for this version, but I am ready to enhance the UI as per feedback.

## Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/prathameshdol196/Single-Vendor-E-Commerce-Website/tree/master
    ```

2. **Navigate to the project directory:**
    ```bash
    cd Single Vendor E-Commerce Website
    ```

3. **Create and activate a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

4. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

5. **Set environment variables:**
    - Create a `.env` file or set environment variables directly.
    ```bash
    export SECRET_KEY='your_secret_key'
    export DATABASE_URL='your_postgresql_database_url'
    export ADMIN_USERNAME='your_admin_username'
    export ADMIN_EMAIL='your_admin_email'
    export ADMIN_PASSWORD='your_admin_password'
    ```

6. **Initialize the database:**
    ```bash
    flask db init
    flask db migrate -m "Initial migration."
    flask db upgrade
    ```

7. **Run the application:**
    ```bash
    python run.py
    ```

## Deployment

Deployed on Render.com: [https://single-vendor-e-commerce-website.onrender.com/](https://single-vendor-e-commerce-website.onrender.com/)

## Screenshots

Screenshots : [Screenshots](https://github.com/prathameshdol196/Single-Vendor-E-Commerce-Website/tree/master/screenshots)

## License

This project is licensed under the MIT License.
