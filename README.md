# eCommerce Application — M06T06

A Django eCommerce web application supporting vendor and buyer user roles.

## Project Structure

```
ecommerce_project/   ← Django project config (settings, urls)
accounts/            ← Custom User model, registration, login, password reset
store/               ← Store, Product, Order, Review models and views
templates/           ← All HTML templates
Planning/            ← System planning documents
research_answers.txt ← Research task answers
```

## Features

- **User Roles**: Register as a vendor or buyer
- **Vendors**: Create, edit, and delete stores and products
- **Buyers**: Browse products, add to cart (session-based), checkout
- **Email Invoice**: Sent automatically on checkout
- **Reviews**: Verified (purchased) and unverified reviews
- **Password Reset**: Secure email-based reset with expiring tokens (Django built-in)
- **Database**: SQLite for development; configure MariaDB/MySQL via `.env`
- **Authentication**: Login required on protected views; vendor-only views enforced

## Setup

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Environment Variables

Copy `.env.example` to `.env` and fill in values for production use:

| Variable | Purpose |
|---|---|
| `DJANGO_SECRET_KEY` | Django secret key |
| `DB_NAME` | MariaDB database name (omit to use SQLite) |
| `DB_USER` | MariaDB username |
| `DB_PASSWORD` | MariaDB password |
| `EMAIL_HOST` | SMTP host (omit to print emails to console) |
| `EMAIL_HOST_USER` | SMTP username |
| `EMAIL_HOST_PASSWORD` | SMTP password |
