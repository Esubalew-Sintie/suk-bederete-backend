# Generated by Django 5.0.2 on 2024-05-12 10:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Template',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('preview_image', models.ImageField(upload_to='images/preview/')),
                ('category', models.CharField(choices=[('electronics', 'Electronics'), ('clothing', 'Clothing'), ('household', 'Household')], max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('html', models.TextField()),
                ('css', models.TextField()),
                ('js', models.TextField()),
                ('template', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pages', to='builder.template')),
            ],
        ),
    ]
