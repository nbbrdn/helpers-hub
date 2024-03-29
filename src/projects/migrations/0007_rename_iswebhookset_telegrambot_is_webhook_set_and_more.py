# Generated by Django 5.0.1 on 2024-01-11 01:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0006_telegrambot_name_telegrambot_username'),
    ]

    operations = [
        migrations.RenameField(
            model_name='telegrambot',
            old_name='isWebhookSet',
            new_name='is_webhook_set',
        ),
        migrations.AlterField(
            model_name='telegrambot',
            name='username',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Username'),
        ),
    ]
