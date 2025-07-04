# Generated by Django 5.2.2 on 2025-06-10 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='specialty',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.CharField(choices=[('Patient', 'Patient'), ('Doctor', 'Doctor'), ('Admin', 'Admin')], max_length=10),
        ),
    ]
