# Generated by Django 4.0.3 on 2022-03-06 12:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0006_remove_trainingtest_customers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trainingtestcustomerrelation',
            name='training_test',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='training_tests', to='training.trainingtest'),
        ),
    ]