# Generated by Django 4.2 on 2024-12-11 18:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('credentials', '0001_initial'),
        ('companies', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='credentials',
            field=models.ManyToManyField(blank=True, to='credentials.credential'),
        ),
    ]