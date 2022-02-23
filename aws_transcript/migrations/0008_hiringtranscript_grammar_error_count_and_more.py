# Generated by Django 4.0.2 on 2022-02-23 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aws_transcript', '0007_hiringnotokgrammererrorlist_hiringokgrammererrorlist_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='hiringtranscript',
            name='grammar_error_count',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='hiringtranscript',
            name='grammar_error_count_per_minute',
            field=models.DecimalField(blank=True, decimal_places=5, max_digits=30, null=True),
        ),
    ]
