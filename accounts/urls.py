from django.urls import path, include
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register, name='register'),
    # Use Django's built-in auth views for login/logout/password reset
    path('', include('django.contrib.auth.urls')),
]
