# Generated by Django 4.2.7 on 2024-11-16 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_remove_cartorderitem_coupons_cartorderitem_coupons'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartorderitem',
            name='coupons',
            field=models.ManyToManyField(blank=True, to='api.coupon'),
        ),
    ]
