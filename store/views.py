from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from .models import Product, Order, OrderItem, Store
from decimal import Decimal
from .forms import StoreForm, ProductForm
from django.http import HttpResponseForbidden


def product_list(request):
    """Display all products available in the store."""
    products = Product.objects.select_related('store').all()
    return render(request, 'store/product_list.html', {'products': products})


@login_required
def vendor_stores(request):
    """Display the vendor's own stores dashboard."""
    if not request.user.is_vendor:
        return HttpResponseForbidden('Vendor access only')
    stores = Store.objects.filter(vendor=request.user)
    return render(request, 'store/vendor_stores.html', {'stores': stores})


@login_required
def store_create(request):
    """Allow a vendor to create a new store."""
    if not request.user.is_vendor:
        return HttpResponseForbidden('Vendor access only')
    if request.method == 'POST':
        form = StoreForm(request.POST)
        if form.is_valid():
            s = form.save(commit=False)
            s.vendor = request.user
            s.save()
            return redirect('store:vendor_stores')
    else:
        form = StoreForm()
    return render(request, 'store/store_form.html', {'form': form})


@login_required
def store_edit(request, pk):
    """Allow the owning vendor to edit a store."""
    store = get_object_or_404(Store, pk=pk)
    if store.vendor != request.user:
        return HttpResponseForbidden('Not your store')
    if request.method == 'POST':
        form = StoreForm(request.POST, instance=store)
        if form.is_valid():
            form.save()
            return redirect('store:vendor_stores')
    else:
        form = StoreForm(instance=store)
    return render(request, 'store/store_form.html', {'form': form})


@login_required
def store_delete(request, pk):
    """Allow the owning vendor to delete a store."""
    store = get_object_or_404(Store, pk=pk)
    if store.vendor != request.user:
        return HttpResponseForbidden('Not your store')
    if request.method == 'POST':
        store.delete()
        return redirect('store:vendor_stores')
    return render(request, 'store/store_confirm_delete.html', {'store': store})


@login_required
def product_create(request, store_pk):
    """Allow a vendor to add a product to one of their stores."""
    store = get_object_or_404(Store, pk=store_pk)
    if store.vendor != request.user:
        return HttpResponseForbidden('Not your store')
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            p = form.save(commit=False)
            p.store = store
            p.save()
            return redirect('store:vendor_stores')
    else:
        form = ProductForm()
    return render(request, 'store/product_form.html', {'form': form, 'store': store})


@login_required
def product_edit(request, pk):
    """Allow the owning vendor to edit a product."""
    p = get_object_or_404(Product, pk=pk)
    if p.store.vendor != request.user:
        return HttpResponseForbidden('Not your product')
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=p)
        if form.is_valid():
            form.save()
            return redirect('store:vendor_stores')
    else:
        form = ProductForm(instance=p)
    return render(request, 'store/product_form.html', {'form': form, 'store': p.store})


@login_required
def product_delete(request, pk):
    """Allow the owning vendor to delete a product."""
    p = get_object_or_404(Product, pk=pk)
    if p.store.vendor != request.user:
        return HttpResponseForbidden('Not your product')
    if request.method == 'POST':
        p.delete()
        return redirect('store:vendor_stores')
    return render(request, 'store/product_confirm_delete.html', {'product': p})


def product_detail(request, pk):
    """Display a single product with its reviews."""
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'store/product_detail.html', {'product': product})


def add_to_cart(request, pk):
    """Add a product to the session-based shopping cart."""
    product = get_object_or_404(Product, pk=pk)
    cart = request.session.get('cart', {})
    cart[str(product.pk)] = cart.get(str(product.pk), 0) + int(request.POST.get('quantity', 1))
    request.session['cart'] = cart
    return redirect('store:cart')


def cart_view(request):
    """Display the current buyer's shopping cart."""
    cart = request.session.get('cart', {})
    items = []
    total = Decimal('0.00')
    for pid, qty in cart.items():
        try:
            p = Product.objects.get(pk=int(pid))
            items.append({'product': p, 'quantity': qty, 'subtotal': p.price * int(qty)})
            total += p.price * int(qty)
        except Product.DoesNotExist:
            pass
    return render(request, 'store/cart.html', {'items': items, 'total': total})


@login_required
def checkout(request):
    """Process the buyer's cart: create an order, reduce stock, and email an invoice."""
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('store:product_list')

    with transaction.atomic():
        order = Order.objects.create(buyer=request.user)
        total = Decimal('0.00')
        for pid, qty in cart.items():
            product = Product.objects.select_for_update().get(pk=int(pid))
            if product.stock < int(qty):
                raise Exception(f"Not enough stock for {product.name}")
            product.stock -= int(qty)
            product.save()
            subtotal = product.price * int(qty)
            OrderItem.objects.create(
                order=order,
                product_name=product.name,
                product_id=product.pk,
                price=product.price,
                quantity=int(qty),
            )
            total += subtotal
        order.total = total
        order.save()

    request.session['cart'] = {}

    subject = f"Invoice for Order #{order.pk}"
    lines = [f"Order #{order.pk}", f"Date: {order.created_at}", "Items:"]
    for item in order.items.all():
        lines.append(f"- {item.product_name} x{item.quantity} @ {item.price}")
    lines.append(f"Total: {order.total}")
    message = "\n".join(lines)
    send_mail(subject, message, None, [request.user.email], fail_silently=False)

    return render(request, 'store/checkout_success.html', {'order': order})


@login_required
def add_review(request, pk):
    """Submit a review for a product; mark as verified if the buyer purchased it."""
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST' and request.user.is_authenticated:
        rating = int(request.POST.get('rating', 5))
        content = request.POST.get('content', '')
        purchased = OrderItem.objects.filter(
            order__buyer=request.user, product_id=product.pk
        ).exists()
        from .models import Review
        Review.objects.create(
            product=product,
            buyer=request.user,
            rating=rating,
            content=content,
            verified=purchased,
        )
    return redirect('store:product_detail', pk=product.pk)
