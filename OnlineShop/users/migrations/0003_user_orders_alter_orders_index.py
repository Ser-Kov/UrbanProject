# Generated by Django 5.1 on 2024-09-06 14:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_orders'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='orders',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.orders'),
        ),
        migrations.AlterField(
            model_name='orders',
            name='index',
            field=models.PositiveIntegerField(),
        ),
    ]
