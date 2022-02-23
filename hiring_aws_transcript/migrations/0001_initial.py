# Generated by Django 4.0.2 on 2022-02-23 12:34

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HiringErrorVideo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video_url', models.TextField()),
                ('error', models.TextField()),
                ('error_date', models.DateTimeField(blank=True, default=datetime.datetime.now)),
            ],
        ),
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
            name='HiringQuestionAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video_type', models.CharField(blank=True, max_length=200, null=True)),
                ('video_type_id', models.IntegerField(blank=True, default=0, null=True)),
                ('questionID', models.CharField(blank=True, max_length=50, null=True)),
                ('question', models.CharField(blank=True, max_length=1500, null=True)),
                ('answer', models.CharField(blank=True, max_length=10000, null=True)),
                ('cleaned_answer', models.TextField(blank=True, default='NA', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='HiringReiviewGrammerErrorList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('error_desc', models.CharField(blank=True, max_length=3500, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='HiringRelevance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transcript', models.TextField()),
                ('Candidate_id', models.CharField(blank=True, max_length=50, null=True)),
                ('questionID', models.CharField(blank=True, max_length=50, null=True)),
                ('video_type_id', models.IntegerField(blank=True, default=0, null=True)),
                ('video_type', models.CharField(blank=True, max_length=200, null=True)),
                ('cleaned_transcript', models.TextField(blank=True, default='NA', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='HiringTranscript',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('response_id', models.CharField(max_length=50)),
                ('Candidate_id', models.CharField(blank=True, max_length=50, null=True)),
                ('questionID', models.CharField(blank=True, max_length=50, null=True)),
                ('video_type_id', models.IntegerField(blank=True, default=0, null=True)),
                ('transcript', models.TextField()),
                ('video_type', models.CharField(blank=True, max_length=200, null=True)),
                ('total_words', models.IntegerField(default=0)),
                ('stutter_count', models.IntegerField(blank=True, default=0, null=True)),
                ('stutter_per_minute', models.DecimalField(blank=True, decimal_places=5, max_digits=30, null=True)),
                ('Words_per_minute', models.DecimalField(blank=True, decimal_places=5, max_digits=30, null=True)),
                ('average_confidence', models.DecimalField(blank=True, decimal_places=5, max_digits=30, null=True)),
                ('speak_time', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('hurriness', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('grammar_error_count', models.IntegerField(blank=True, default=0, null=True)),
                ('grammar_error_count_per_minute', models.DecimalField(blank=True, decimal_places=5, max_digits=30, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='HiringVideoIdToVideoTypeMaping',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video_type_id', models.IntegerField(blank=True, default=0, null=True)),
                ('video_type', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='HiringWord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('end_time', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('content', models.CharField(blank=True, max_length=30, null=True)),
                ('pron', models.CharField(blank=True, max_length=30, null=True)),
                ('confidence', models.DecimalField(blank=True, decimal_places=4, max_digits=5, null=True)),
                ('mean_time', models.DecimalField(blank=True, decimal_places=5, max_digits=30, null=True)),
                ('second', models.IntegerField(default=0)),
                ('video_type', models.CharField(blank=True, max_length=200, null=True)),
                ('is_stutter', models.BooleanField(blank=True, default=False, null=True)),
                ('transcript_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='word_details', to='hiring_aws_transcript.hiringtranscript')),
            ],
        ),
    ]