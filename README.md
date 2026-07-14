````markdown
# 🏆 Hadi Sports - Sports E-Commerce Platform

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.x-success.svg)](https://www.djangoproject.com/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5-purple.svg)](https://getbootstrap.com/)
[![Status](https://img.shields.io/badge/Status-Production-orange.svg)]()

Hadi Sports is a modern sports e-commerce website developed with Django for a sports retail business. Customers can browse sports products, add one or multiple items to their shopping cart, and place orders directly through WhatsApp without creating an account.

---

# 🚀 Live Demo

**Coming Soon**

---

# ✨ Features

## 🛍️ Shopping Features

- Sports Product Catalog
- Product Categories
- Product Details Page
- Product Search
- Session-Based Shopping Cart
- Multiple Product Selection
- WhatsApp Order Checkout
- Responsive Design
- Fast Loading
- Mobile Friendly

---

## 🛒 Order Flow

1. Browse Products
2. View Product Details
3. Add Products to Cart
4. Update Cart Quantity
5. Proceed to Checkout
6. Enter Customer Details
7. Confirm Order
8. Order Sent Directly to WhatsApp

---

# 🛠 Technology Stack

## Backend

- Python 3
- Django 5
- SQLite (Development)
- PostgreSQL (Production)

## Frontend

- HTML5
- CSS3
- Bootstrap 5
- JavaScript
- jQuery
- Django Templates

---

# 📂 Project Structure

```text
hadi_sports/
│
├── apps/
│   ├── core/
│   ├── pages/
│   ├── products/
|    |            │
|    |            ├── product_category.py
|    |            │
|   |            ├── product.py
    |            │
    |            ├── product_option.py
    |
    |           │
    |            ├── product_variant.py
    |            │
    |            └── variant_image.py
│   ├── cart/
│   ├── orders/
│   └── contact/
│
├── config/
├── templates/
├── static/
├── media/
├── staticfiles/
├── requirements.txt
├── .gitignore
├── .env
├── README.md
└── manage.py
```
ProductCategory
      │
      │
      ▼
Product
      │
      ├──────────────┐
      │              │
      ▼              ▼
ProductOption    ProductVariant
      │              │
      ▼              ▼
ProductOptionValue  VariantImage
---

# ⚙️ Installation

## Clone Repository

```bash
git clone https://github.com/MuhammadNouman769/hadisports.git
cd hadisports
```

## Create Virtual Environment

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

## Create Superuser

```bash
python manage.py createsuperuser
```

## Run Development Server

```bash
python manage.py runserver
```

Open your browser:

```
http://127.0.0.1:8000/
```

---

# 📦 Requirements

- Python 3.12+
- Django 5+
- Pillow
- python-decouple

```bash
pip install -r requirements.txt
```

---

# 📱 WhatsApp Ordering

Customers can:

- Browse sports products.
- Add one or multiple products to the shopping cart.
- Enter their contact information.
- Confirm their order.
- Automatically send the complete order to the store's WhatsApp number.

---

# 📷 Screenshots

Project screenshots will be added after deployment.

---

# 🏢 Developed By

## BTR Solutions

**BTR Solutions** is a software development company focused on delivering high-quality digital solutions for businesses of all sizes. We specialize in developing scalable, secure, and modern software tailored to each client's unique business requirements.

### Our Expertise

- Custom Web Application Development
- E-Commerce Solutions
- Django & Python Development
- REST API Development
- Business Management Systems
- Inventory & POS Solutions
- Mobile Application Development
- UI/UX Design
- Website Maintenance & Technical Support

---

```markdown
# 👨‍💻 Founder & CEO — BTR Solutions

**Muhammad Nouman**

Founder & CEO | Full Stack Software Engineer

### Core Technologies

- Python
- Django
- Django REST Framework (DRF)
- JavaScript (ES6+)
- React.js
- React Native
- HTML5
- CSS3
- Bootstrap 5
- Tailwind CSS
- PostgreSQL
- MySQL
- SQLite
- Redis
- Celery
- REST APIs
- Git & GitHub
- Linux (Ubuntu)
- Docker
- Nginx
- Gunicorn

### Expertise

- Custom Web Applications
- Enterprise Software Development
- E-Commerce Platforms
- Multi-Vendor Marketplace Solutions
- Business Management Systems (ERP/CRM)
- Inventory & POS Systems
- Mobile Application Development
- API Development & Integration
- Database Design & Optimization
- Deployment & Server Management
- Performance Optimization
- Software Architecture

GitHub: https://github.com/MuhammadNouman769
```

---

# 📄 Commercial Project Notice

This project has been custom-designed and developed by **BTR Solutions** for a sports retail business under a commercial software development agreement.

The software, source code, application architecture, UI/UX design, documentation, and all associated assets are proprietary and confidential. Unauthorized copying, redistribution, modification, reverse engineering, resale, or commercial reuse of this project, in whole or in part, without prior written authorization from **BTR Solutions** and the project owner is strictly prohibited.

---

# 🤝 Business Inquiries

For custom software development, enterprise applications, e-commerce platforms, business automation systems, or long-term technical partnerships, please contact **BTR Solutions**.

---

# © Copyright

© 2026 **BTR Solutions**. All Rights Reserved.

Developed with ❤️ by **BTR Solutions**.
````
