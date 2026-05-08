from django.urls import path, include
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    # Django built-in auth views (login, password reset, etc.)
    path('', include('django.contrib.auth.urls')),
]
