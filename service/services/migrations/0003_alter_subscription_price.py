# Generated by Django 3.2.16 on 2024-03-23 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0002_subscription_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='price',
            field=models.PositiveIntegerField(db_index=True, default=0),
        ),
    ]
