# Generated by Django 3.0.1 on 2020-04-27 03:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0002_auto_20200426_0617'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='name',
            field=models.CharField(max_length=200),
        ),
    ]