# Generated by Django 2.1.1 on 2018-12-07 22:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_compquiz'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='compquiz',
            name='Class',
        ),
        migrations.RemoveField(
            model_name='compquiz',
            name='invited_instructor',
        ),
        migrations.RemoveField(
            model_name='compquiz',
            name='quiz',
        ),
        migrations.DeleteModel(
            name='CompQuiz',
        ),
    ]
