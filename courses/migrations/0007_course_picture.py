# Generated by Django 4.0.3 on 2022-03-03 07:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0006_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to='course_images/'),
        ),
    ]
