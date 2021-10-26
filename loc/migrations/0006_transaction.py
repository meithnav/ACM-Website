# Generated by Django 3.1.7 on 2021-03-19 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loc', '0005_auto_20210319_0135'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.CharField(max_length=20, unique=True)),
                ('made_on', models.DateTimeField(auto_now_add=True)),
                ('amount', models.IntegerField()),
                ('order_id', models.CharField(blank=True, max_length=100, null=True, unique=True)),
                ('checksum', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
    ]
