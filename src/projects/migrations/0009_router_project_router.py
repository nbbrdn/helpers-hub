# Generated by Django 5.0.1 on 2024-01-17 03:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0008_alter_supervisor_phone'),
    ]

    operations = [
        migrations.CreateModel(
            name='Router',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name='Name')),
                ('handler', models.CharField(max_length=50, verbose_name='handler')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создан')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Изменён')),
            ],
            options={
                'verbose_name': 'Router',
                'verbose_name_plural': 'Routers',
                'ordering': ['-created_at'],
            },
        ),
        migrations.AddField(
            model_name='project',
            name='router',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='projects', to='projects.router'),
        ),
    ]
