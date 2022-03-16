# Generated by Django 4.0 on 2021-12-25 15:49

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_homeworkanswer'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mark',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mark', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='Mark')),
                ('homework_answer', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='mark', to='courses.homeworkanswer')),
            ],
        ),
    ]
