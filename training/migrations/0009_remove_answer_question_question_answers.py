# Generated by Django 4.0.3 on 2022-03-06 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0008_remove_question_answers_answer_question'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='answer',
            name='question',
        ),
        migrations.AddField(
            model_name='question',
            name='answers',
            field=models.ManyToManyField(related_name='questions', to='training.answer'),
        ),
    ]
