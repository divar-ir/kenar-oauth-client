# Generated by Django 4.2.4 on 2023-08-16 13:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Oauth',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('access_token', models.CharField(max_length=128)),
                ('refresh_token', models.CharField(max_length=256)),
                ('expires', models.DateTimeField()),
                ('phone', models.CharField(max_length=11)),
                ('session_id', models.CharField(max_length=128, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Scope',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('permission_type', models.CharField(choices=[('ADDON_USER_APPROVED', 'ADDON_USER_APPROVED'), ('USER_PHONE', 'USER_PHONE')], max_length=100)),
                ('resource_id', models.CharField(max_length=100, null=True)),
                ('oauth', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='handler.oauth')),
            ],
        ),
    ]
