import stripe
from rest_framework.response import Response

from . import models as db_models
from django.views.generic import DetailView, ListView
from rest_framework.views import APIView
from . import serializers
from .utils.cart import Cart


class ItemListView(ListView):
    model = db_models.Item
    template_name = 'shop/item_list.html'


class ItemDetailView(DetailView):
    model = db_models.Item
    template_name = 'shop/item_detail.html'


class CreatePaymentIntentView(APIView):
    def post(self, request):
        item_list_serializer = serializers.ItemListSerializer(request.data)
        item_ids: list[int] = item_list_serializer.instance.get('item_ids')
        items = db_models.Item.objects.filter(id__in=item_ids)
        order = db_models.Order.objects.create()
        order.items.add(*items)
        order.save()

        payment_intent = stripe.PaymentIntent.create(
            amount=order.get_price(),
            currency='usd',
            automatic_payment_methods={
                'enabled': True
            }
        )
        return Response({'client_secret': payment_intent.client_secret})
