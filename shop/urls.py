from django.urls import path
from . import views


urlpatterns = [
    path('item/<int:pk>', views.ItemDetail.as_view(), name='item_detail'),
    path('items/', views.ItemList.as_view(), name='item_list'),
]
