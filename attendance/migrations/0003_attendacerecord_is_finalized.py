# Generated by Django 5.0.4 on 2024-10-19 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0002_alter_attendacerecord_date_attendancerequest'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendacerecord',
            name='is_finalized',
            field=models.BooleanField(default=True),
        ),
    ]
