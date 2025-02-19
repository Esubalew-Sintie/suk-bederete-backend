# Generated by Django 5.0.6 on 2024-07-02 22:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_account_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='role',
            field=models.CharField(choices=[('customer', 'Customer'), ('merchant', 'Merchant'), ('admin', 'Admin')], default='customer', max_length=10),
        ),
    ]
