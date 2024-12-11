# Generated by Django 4.2 on 2024-12-10 15:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('credentials', '0001_initial'),
        ('companies', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='company_owner',
            field=models.CharField(default=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL), max_length=30),
        ),
        migrations.AddField(
            model_name='company',
            name='credentials',
            field=models.ManyToManyField(to='credentials.credential'),
        ),
    ]