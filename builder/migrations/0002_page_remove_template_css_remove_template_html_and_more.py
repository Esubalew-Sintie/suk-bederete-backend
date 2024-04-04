# Generated by Django 5.0.2 on 2024-04-04 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('builder', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('html', models.TextField()),
                ('css', models.TextField()),
                ('js', models.TextField()),
            ],
        ),
        migrations.RemoveField(
            model_name='template',
            name='css',
        ),
        migrations.RemoveField(
            model_name='template',
            name='html',
        ),
        migrations.RemoveField(
            model_name='template',
            name='js',
        ),
        migrations.AddField(
            model_name='template',
            name='pages',
            field=models.ManyToManyField(related_name='pages', to='builder.page'),
        ),
    ]
