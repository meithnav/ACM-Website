# Generated by Django 3.1.7 on 2021-03-27 06:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('if', '0004_formstudent_stu_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='formstudent',
            name='stu_id',
        ),
    ]
