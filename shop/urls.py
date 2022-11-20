from django.urls import path
from . import views


urlpatterns = [
    path('item/<int:pk>', views.ItemDetailView.as_view(), name='item_detail'),
    path('items/', views.ItemListView.as_view(), name='item_list'),
    path('create_intent/', views.CreatePaymentIntentView.as_view(), name='create_intent'),
    path('cart/', views.CartView.as_view(), name='cart_view')
]
