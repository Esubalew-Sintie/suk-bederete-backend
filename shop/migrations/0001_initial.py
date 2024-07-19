# Generated by Django 5.0.6 on 2024-07-19 11:49

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('builder', '0001_initial'),
        ('merchant', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Picture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='pictures/')),
            ],
        ),
        migrations.CreateModel(
            name='Screenshot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images/screenshots/')),
                ('caption', models.CharField(blank=True, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='CustomizedTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modifiedby', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customized_templates', to='merchant.merchant')),
                ('original_template', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='builder.template')),
            ],
        ),
        migrations.CreateModel(
            name='CustomizedPage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('html', models.TextField()),
                ('css', models.TextField()),
                ('js', models.TextField()),
                ('customized_template', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pages', to='shop.customizedtemplate')),
            ],
        ),
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('preview_image', models.ImageField(blank=True, null=True, upload_to='images/preview/')),
                ('unique_id', models.CharField(blank=True, editable=False, max_length=255, unique=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('customized_template', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.customizedtemplate')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='merchant.merchant')),
            ],
        ),
        migrations.CreateModel(
            name='ShopRating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField()),
                ('comment', models.TextField(blank=True, null=True)),
                ('ip', models.CharField(blank=True, max_length=20)),
                ('status', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('shop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to='shop.shop')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
