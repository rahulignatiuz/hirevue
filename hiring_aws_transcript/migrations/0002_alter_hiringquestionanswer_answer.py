# Generated by Django 4.0.2 on 2022-02-24 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hiring_aws_transcript', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hiringquestionanswer',
            name='answer',
            field=models.TextField(blank=True, default='NA', null=True),
        ),
    ]