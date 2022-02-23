# Generated by Django 4.0.2 on 2022-02-22 07:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aws_transcript', '0002_transcript_candidate_id_transcript_words_per_minute_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuestionAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video_type', models.CharField(blank=True, max_length=200, null=True)),
                ('video_type_id', models.IntegerField(blank=True, default=0, null=True)),
                ('questionID', models.CharField(blank=True, max_length=50, null=True)),
                ('question', models.CharField(blank=True, max_length=150, null=True)),
                ('answer', models.CharField(blank=True, max_length=500, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='transcript',
            name='video_type_id',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]