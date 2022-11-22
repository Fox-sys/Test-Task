from rest_framework import serializers
from . import models as db_models


class CartItemAddSerializer(serializers.Serializer):
    item_id = serializers.IntegerField()
    amount = serializers.IntegerField(default=1)
    update_amount = serializers.BooleanField(default=False)


class CartItemRemoveSerializer(serializers.Serializer):
    item_id = serializers.IntegerField()


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = db_models.Item
        fields = ['id', 'name', 'currency', 'price']