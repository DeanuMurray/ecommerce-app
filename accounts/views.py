from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import UserRegisterForm


def register(request):
    """Register a new user as a vendor or buyer.

    On POST, validate the registration form, create the user, log them
    in, and redirect to the product list.  On GET, display an empty form.
    """
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('store:product_list')
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


def logout_view(request):
    """Log the current user out and redirect to the login page."""
    if request.method == 'POST':
        logout(request)
    return redirect('accounts:login')
