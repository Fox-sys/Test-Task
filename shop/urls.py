from django.urls import path
from . import views


urlpatterns = [
    path('item/<int:pk>', views.ItemDetailView.as_view(), name='item_detail'),
    path('', views.ItemListView.as_view(), name='item_list'),
    path('payment/', views.PaymentView.as_view(), name='payment_view'),
    path('cart/', views.CartView.as_view(), name='cart_view'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout_view'),
    path('webhook/stripe/', views.WebHook.as_view(), name='webhook_url')
]
