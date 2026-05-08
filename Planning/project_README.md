# eCommerce Project (M06T06) — Project README

This is a scaffold for the HyperionDev eCommerce task. Follow the Planning document in this folder.

Setup (development):

1. Create a virtual environment and install requirements:
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt

2. Run migrations:
   python manage.py makemigrations
   python manage.py migrate

3. Create a superuser:
   python manage.py createsuperuser

4. Run the dev server:
   python manage.py runserver

Run tests:
   python manage.py test

Notes:
- The project contains a minimal implementation of vendor and buyer flows, session-cart, checkout with invoice email (console backend by default), password reset via email (token expires per `PASSWORD_RESET_TIMEOUT` in settings), and review verification logic.
- Place the completed project under `M06T06/` for submission. Ensure you run migrations and configure your DB and email backends for production use.

DB notes: default is `sqlite3` for development. This project supports using MariaDB/MySQL by setting environment variables in a `.env` file (see `.env.example`) and the settings will automatically switch the database engine when `DB_NAME` is present.

Email: If you set `EMAIL_HOST` in `.env` the project will use SMTP (configure `EMAIL_PORT`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, `EMAIL_USE_TLS`). If `EMAIL_HOST` is not set, the project uses the console email backend (good for development).
