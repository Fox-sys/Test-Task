from . import models as db_models
from django.views.generic import DetailView, ListView


class ItemList(ListView):
    model = db_models.Item
    template_name = 'shop/item_list.html'


class ItemDetail(DetailView):
    model = db_models.Item
    template_name = 'shop/item_detail.html'
