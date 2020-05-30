# Generated by Django 3.0.3 on 2020-05-29 01:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Results',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('provider_id', models.CharField(blank=True, default='', max_length=100)),
                ('measure_id', models.CharField(blank=True, default='', max_length=100)),
                ('performance_class', models.CharField(blank=True, default='', max_length=100)),
            ],
        ),
    ]
