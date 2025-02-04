from django.urls import path
from .views import HomeView, ChannelDetailView, product_detail

app_name = 'channel'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('<int:pk>/', ChannelDetailView.as_view(), name='detail'),
    path('product/<int:pk>/', product_detail, name='product-detail'),
]
