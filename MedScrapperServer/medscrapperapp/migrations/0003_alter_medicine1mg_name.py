# Generated by Django 4.1.6 on 2023-02-21 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medscrapperapp', '0002_subscription'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medicine1mg',
            name='name',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]