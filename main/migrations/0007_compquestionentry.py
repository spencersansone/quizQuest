# Generated by Django 2.1.1 on 2018-12-09 23:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_compquizentry'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompQuestionEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comp_quiz_entry', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='main.CompQuizEntry')),
                ('correct_answer', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='correct_comp_answer', to='main.Answer')),
                ('selected_answer', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='selected_comp_answer', to='main.Answer')),
            ],
        ),
    ]