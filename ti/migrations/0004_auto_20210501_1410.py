# Generated by Django 3.2 on 2021-05-01 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ti', '0003_auto_20210425_1433'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Car',
        ),
        migrations.AlterField(
            model_name='track',
            name='id',
            field=models.CharField(max_length=22, primary_key=True, serialize=False),
        ),
    ]
