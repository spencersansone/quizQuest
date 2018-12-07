# Generated by Django 2.1.1 on 2018-12-07 22:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20181207_2224'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompQuiz',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('approved', models.BooleanField()),
                ('declined', models.BooleanField()),
                ('Class', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='main.Class')),
                ('invited_instructor', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='main.UserProfile')),
                ('quiz', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='main.Quiz')),
            ],
        ),
    ]
