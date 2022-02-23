# Generated by Django 4.0.2 on 2022-02-23 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aws_transcript', '0006_hiringrelevance_cleaned_transcript'),
    ]

    operations = [
        migrations.CreateModel(
            name='HiringNotOkGrammerErrorList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('error_desc', models.CharField(blank=True, max_length=3500, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='HiringOkGrammerErrorList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('error_desc', models.CharField(blank=True, max_length=3500, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='HiringReiviewGrammerErrorList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('error_desc', models.CharField(blank=True, max_length=3500, null=True)),
            ],
        ),
    ]