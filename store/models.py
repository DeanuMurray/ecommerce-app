from django.db import models
from django.conf import settings
from decimal import Decimal


class Store(models.Model):
    """A store owned by a vendor user."""

    vendor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return the store name."""
        return self.name


class Product(models.Model):
    """A product listed in a store."""

    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    stock = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return the product name."""
        return self.name


class Order(models.Model):
    """A completed purchase order placed by a buyer."""

    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))

    def __str__(self):
        """Return a human-readable order identifier."""
        return f"Order #{self.pk} by {self.buyer.username}"


class OrderItem(models.Model):
    """A single line item within an Order."""

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product_name = models.CharField(max_length=255)
    product_id = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        """Return quantity and product name."""
        return f"{self.quantity} x {self.product_name}"


class Review(models.Model):
    """A buyer review for a product, verified if the buyer purchased it."""

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    rating = models.PositiveSmallIntegerField(default=5)
    content = models.TextField()
    verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return reviewer name and verification status."""
        return f"Review by {self.buyer} ({'verified' if self.verified else 'unverified'})"
