# Generated by Django 5.0.6 on 2024-07-02 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('merchant', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='merchant',
            name='unique_id',
            field=models.CharField(editable=False, max_length=20, primary_key=True, serialize=False, unique=True),
        ),
    ]
