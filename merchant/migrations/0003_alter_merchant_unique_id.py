# Generated by Django 5.0.6 on 2024-07-18 17:42

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('merchant', '0002_alter_merchant_unique_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='merchant',
            name='unique_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True),
        ),
    ]
