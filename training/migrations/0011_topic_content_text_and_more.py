# Generated by Django 4.0.3 on 2022-03-06 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0010_rename_correct_answers_trainingtestcustomerrelation_correct_answers_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='content_text',
            field=models.TextField(default='Super content'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='trainingtestcustomerrelation',
            name='passed',
            field=models.BooleanField(default=False),
        ),
    ]
