# Generated by Django 3.1.5 on 2021-01-06 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questionAns', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdata',
            name='user_type',
            field=models.CharField(default='woner', max_length=10),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='userdata',
            name='user_id',
            field=models.CharField(max_length=40),
        ),
    ]
