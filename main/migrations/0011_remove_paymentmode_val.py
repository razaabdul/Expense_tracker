# Generated by Django 4.2.4 on 2023-09-08 12:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_category_val_paymentmode_val'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paymentmode',
            name='val',
        ),
    ]
