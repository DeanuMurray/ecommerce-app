from django.test import TestCase, Client, override_settings
from django.contrib.auth import get_user_model
from .models import Product, Store, Order, OrderItem, Review
from django.urls import reverse
from decimal import Decimal

User = get_user_model()


class StoreTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.vendor = User.objects.create_user(username='vendor', password='pass', is_vendor=True)
        self.buyer = User.objects.create_user(username='buyer', password='pass', email='buyer@example.com')
        self.store = Store.objects.create(vendor=self.vendor, name='Vendor Store')
        self.product = Product.objects.create(store=self.store, name='Prod', price=Decimal('10.00'), stock=5)

    def test_review_verified_if_purchased(self):
        # create order and orderitem
        order = Order.objects.create(buyer=self.buyer, total=Decimal('10.00'))
        OrderItem.objects.create(order=order, product_name=self.product.name, product_id=self.product.pk, price=self.product.price, quantity=1)
        self.client.login(username='buyer', password='pass')
        resp = self.client.post(reverse('store:add_review', args=(self.product.pk,)), {'rating': 5, 'content': 'Great'})
        self.assertEqual(Review.objects.count(), 1)
        r = Review.objects.first()
        self.assertTrue(r.verified)

    @override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
    def test_checkout_creates_order_and_sends_email(self):
        self.client.login(username='buyer', password='pass')
        session = self.client.session
        session['cart'] = {str(self.product.pk): 2}
        session.save()
        resp = self.client.post(reverse('store:checkout'))
        self.assertEqual(Order.objects.count(), 1)
        order = Order.objects.first()
        self.assertEqual(order.total, Decimal('20.00'))
        p = Product.objects.get(pk=self.product.pk)
        self.assertEqual(p.stock, 3)
        # Check mail outbox
        from django.core.mail import outbox
        self.assertEqual(len(outbox), 1)
        self.assertIn('Invoice for Order', outbox[0].subject)
