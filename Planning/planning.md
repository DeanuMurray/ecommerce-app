# eCommerce App — Planning Document

## 1. Overview & Goals
Build an eCommerce web app that allows users to register as **vendors** or **buyers**. Vendors can manage stores and products; buyers can browse, add to cart, checkout, and leave reviews (verified/unverified). The system will support session-based carts, email invoices on checkout, password reset via email tokens, and role-based permissions.

---
## 2. Users & Requirements
- **Unauthenticated visitor**
  - Browse stores and products
  - View product details and reviews
  - Register as buyer or vendor

- **Buyer (authenticated)**
  - View and search products across stores
  - Add products to a session-based cart
  - Checkout (creates an order, reduces stock, generates an invoice, sends email)
  - Leave reviews (marked verified if the buyer purchased the product)
  - Reset forgotten passwords via email link with expiring token

- **Vendor (authenticated)**
  - Create, view, edit, delete Stores
  - Add/edit/remove Products within their stores
  - View orders pertaining to their products (future enhancement)

- **Admin**
  - Manage users, stores, products, and reviews via Django admin

---
## 3. UI / UX Plan
- Header with logo, navigation links (Home, Stores, Cart, Login/Register, My Account)
- Home: featured stores and products
- Store listing & store detail pages
- Product listing & product detail pages with add-to-cart button and reviews
- Cart page: session contents with qty controls and checkout button
- Vendor dashboard: list of stores, create store, store detail with product list and CRUD actions
- Forms: clear labels, validation messages, and confirmation dialogs

Wireframes: simple responsive layout with clear CTAs, minimal steps to checkout.

---
## 4. Access Control & Security
- Use Django's authentication system with a custom `User` model (field `is_vendor` boolean).
- Use `@login_required` and decorator checks (or Django permissions) to restrict vendor-only views.
- Store sensitive settings in environment variables (.env) and do not commit secrets.
- Use HTTPS in production. Enforce secure session cookies (Secure, HttpOnly, SameSite).
- Passwords stored by Django's robust hashing system (PBKDF2 by default).
- Password-reset implemented using Django's token system; configure `PASSWORD_RESET_TIMEOUT` explicitly.
- Email configuration: support console backend for development; provide SMTP/Mailgun instructions for production.
- Protect against CSRF (Django provides middleware), input validation, and use parameterized queries via ORM.
- Rate-limit auth endpoints (optional) to avoid brute-force attacks.
- Database backups, migrations, and least-privileges DB user.

---
## 5. Failure & Recovery Plan
- Wrap checkout operations in DB transactions; if any step fails (e.g., insufficient stock or email failure), rollback to preserve consistency.
- If invoice email fails, keep the order and enqueue retry attempts; notify user about delayed email.
- Graceful error pages (500/404) with friendly messages; log errors with stack traces to file or logging service.
- Implement validation and unit/integration tests for critical flows (checkout, review verification, password reset).
- Monitor system metrics and set up alerts for key failures (database down, email failures).

---
## 6. Tech Stack & Deployment Notes
- Backend: Django (Python)
- DB: MariaDB (preferred) or PostgreSQL / SQLite (dev)
- Email: SMTP (production) or Django Console for dev
- Sessions: Django session framework (database-backed by default)
- Deployment: Docker + Docker Compose (optional), or host on a VPS with Nginx+Gunicorn

---
## 7. Data Model (high level)
- User (custom): username, email, password, is_vendor (bool)
- Store: vendor (FK User), name, description
- Product: store (FK), title, description, price, stock
- Order: buyer (FK User), created_at, total
- OrderItem: order (FK), product snapshot, quantity, price
- Review: product (FK), buyer (FK), rating, content, verified (bool)

---
## 8. Acceptance Criteria / User Stories (sample)
- As a visitor I can register as buyer or vendor.
- As a vendor I can create a store and manage products in it, and cannot edit another vendor's stores.
- As a buyer I can add items to a cart (session), checkout to create an order, receive an invoice email, and see purchased reviews marked as verified.
- As a user I can request a password reset email with a link that expires.

---
## 9. Deliverables
- Project placed under `M06T06/` with Django project and apps.
- `Planning/` including this document.
- README with setup and DB configuration instructions, plus migration steps.
- Basic test coverage of critical flows (checkout, review verification, password reset).

---
*Created for HyperionDev task — place implementation under `M06T06/` as required.*
