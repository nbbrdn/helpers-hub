# Generated by Django 5.0.1 on 2024-01-10 20:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TelegramBot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bot_type', models.CharField(choices=[('dev', 'Development'), ('prod', 'Production'), ('fab', 'Fabric')], default='dev', max_length=20, verbose_name='Bot Type')),
                ('telegram_key', models.CharField(max_length=250, verbose_name='Telegram Key')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bots', to='projects.project')),
            ],
        ),
    ]
