from rest_framework import serializers


class ItemListSerializer(serializers.Serializer):
    item_ids = serializers.ListField()
