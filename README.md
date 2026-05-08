# eCommerce Application — M06T06

A Django eCommerce web application supporting vendor and buyer user roles.

## Project Structure

```
ecommerce_project/   ← Django project config (settings, urls)
accounts/            ← Custom User model, registration, login, password reset
store/               ← Store, Product, Order, Review models and views
templates/           ← All HTML templates (base.html, registration/, accounts/, store/)
static/css/          ← CSS stylesheet
Planning/            ← System planning documents
research_answers.txt ← Research task answers
```

## Setup

```bash
git clone https://github.com/DeanuMurray/ecommerce-app.git
cd ecommerce-app
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Visit http://127.0.0.1:8000/

## Environment Variables

Copy `.env.example` to `.env` and fill in values:

| Variable | Purpose |
|---|---|
| `DJANGO_SECRET_KEY` | Django secret key |
| `DB_NAME` | MariaDB database name (omit to use SQLite) |
| `DB_USER` | MariaDB username |
| `DB_PASSWORD` | MariaDB password |
| `EMAIL_HOST` | SMTP host (omit to print emails to console) |
| `EMAIL_HOST_USER` | SMTP username |
| `EMAIL_HOST_PASSWORD` | SMTP password |

## Features

- Register as a **vendor** (create/edit/delete stores and products) or **buyer** (browse, cart, checkout)
- Session-based shopping cart
- Invoice emailed on checkout
- Verified and unverified product reviews
- Password reset via email
- Role-aware navigation: vendors see "My Stores", buyers see "Cart"
