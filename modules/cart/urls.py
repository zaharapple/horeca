from django.urls import path
from .views import CartView, AddToCartView, RemoveFromCartView, ClearCartView

app_name = 'cart'

urlpatterns = [
    path('', CartView.as_view(), name='view_cart'),
    path('add/<int:product_id>/', AddToCartView.as_view(), name='add_to_cart'),
    path('remove/<int:product_id>/', RemoveFromCartView.as_view(), name='remove_from_cart'),
    path('clear/', ClearCartView.as_view(), name='clear_cart'),
]
