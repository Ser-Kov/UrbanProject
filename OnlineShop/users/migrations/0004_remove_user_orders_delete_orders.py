# Generated by Django 5.1 on 2024-09-06 15:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_user_orders_alter_orders_index'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='orders',
        ),
        migrations.DeleteModel(
            name='Orders',
        ),
    ]
