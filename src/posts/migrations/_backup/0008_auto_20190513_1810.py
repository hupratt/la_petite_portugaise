# Generated by Django 2.2 on 2019-05-13 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0007_auto_20190513_1810'),
    ]

    operations = [
        migrations.AlterField(
            model_name='Post',
            name='body',
            field=models.TextField(unique=True),  # unique=True
            preserve_default=False,
        ),
    ]