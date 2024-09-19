# Generated by Django 5.1.1 on 2024-09-19 06:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trip', '0002_alter_trip_destination'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itineraryitem',
            name='item_type',
            field=models.CharField(choices=[('transport', 'Transport'), ('lodge', 'Lodge'), ('activities', 'Activities')], max_length=75),
        ),
    ]
