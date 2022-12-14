# Generated by Django 4.1.3 on 2022-11-23 10:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_alter_discount_options_alter_order_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tax',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveIntegerField(verbose_name='Цена налога')),
            ],
            options={
                'verbose_name': 'Налог',
                'verbose_name_plural': 'Налоги',
            },
        ),
        migrations.AddField(
            model_name='discount',
            name='amount',
            field=models.PositiveIntegerField(verbose_name='Цена скидки', default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='tax',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.tax'),
        ),
    ]
