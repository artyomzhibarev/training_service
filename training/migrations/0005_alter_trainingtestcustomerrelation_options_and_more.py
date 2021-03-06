# Generated by Django 4.0.3 on 2022-03-06 11:55

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('training', '0004_trainingtestcustomerrelation_correct_answers'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='trainingtestcustomerrelation',
            options={'verbose_name': 'Test result', 'verbose_name_plural': 'Test results'},
        ),
        migrations.RemoveField(
            model_name='trainingtest',
            name='customers',
        ),
        migrations.AddField(
            model_name='trainingtest',
            name='customers',
            field=models.ManyToManyField(related_name='customer_tests', to=settings.AUTH_USER_MODEL),
        ),
    ]
