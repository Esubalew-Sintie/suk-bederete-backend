# Generated by Django 5.0.6 on 2024-07-03 01:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('merchant', '0002_alter_merchant_bank_account_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='merchant',
            name='bank_account_number',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
