# Generated by Django 2.1.7 on 2019-05-27 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_auto_20190503_1912'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='dir',
            field=models.FileField(default=0, upload_to='files/'),
            preserve_default=False,
        ),
    ]
