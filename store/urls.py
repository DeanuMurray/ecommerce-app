from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('product/<int:pk>/review/', views.add_review, name='add_review'),
    path('cart/', views.cart_view, name='cart'),
    path('add-to-cart/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('checkout/', views.checkout, name='checkout'),

    # Vendor URLs
    path('vendor/stores/', views.vendor_stores, name='vendor_stores'),
    path('vendor/store/create/', views.store_create, name='store_create'),
    path('vendor/store/<int:pk>/edit/', views.store_edit, name='store_edit'),
    path('vendor/store/<int:pk>/delete/', views.store_delete, name='store_delete'),

    path('vendor/store/<int:store_pk>/product/create/', views.product_create, name='product_create'),
    path('vendor/product/<int:pk>/edit/', views.product_edit, name='product_edit'),
    path('vendor/product/<int:pk>/delete/', views.product_delete, name='product_delete'),
]
