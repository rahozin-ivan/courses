# Generated by Django 3.2.12 on 2022-03-03 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0007_course_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='homework',
            name='average_mark',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
    ]
