# Generated by Django 3.0.10 on 2020-10-21 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flights', '0002_auto_20201021_2302'),
    ]

    operations = [
        migrations.AlterField(
            model_name='airport',
            name='code',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='airport',
            name='name',
            field=models.CharField(max_length=50),
        ),
    ]
