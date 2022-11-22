from django.contrib import admin
from django.forms import CheckboxSelectMultiple
from django.db import models
from . import models as db_models


@admin.register(db_models.Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'id', 'name', 'price')
    search_fields = ('id', 'name')


@admin.register(db_models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'id', )
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }


@admin.register(db_models.Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'id', )
