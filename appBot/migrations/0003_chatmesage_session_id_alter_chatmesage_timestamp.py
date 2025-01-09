# Generated by Django 5.0.6 on 2024-12-30 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appBot', '0002_chatmesage'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatmesage',
            name='session_id',
            field=models.CharField(default='default_session_id', max_length=255),
        ),
        migrations.AlterField(
            model_name='chatmesage',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]