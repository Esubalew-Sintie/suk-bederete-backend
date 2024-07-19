# Generated by Django 5.0.6 on 2024-07-02 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0002_remove_customer_id_customer_unique_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='address1',
            field=models.CharField(blank=True, max_length=1024, null=True, verbose_name='Address line 1'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='city',
            field=models.CharField(blank=True, max_length=1024, null=True, verbose_name='City'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='country',
            field=models.CharField(blank=True, max_length=1024, null=True, verbose_name='Country'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='name',
            field=models.CharField(blank=True, max_length=1024, null=True, verbose_name='Full name'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='unique_id',
            field=models.CharField(blank=True, editable=False, max_length=50, primary_key=True, serialize=False, unique=True, verbose_name='unique id'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='zip_code',
            field=models.CharField(blank=True, max_length=12, null=True, verbose_name='ZIP'),
        ),
    ]
