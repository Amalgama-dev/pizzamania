# Generated by Django 4.0.1 on 2022-01-26 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_alter_category_options_remove_cart_final_price_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='in_order',
            field=models.BooleanField(default=False),
        ),
    ]
