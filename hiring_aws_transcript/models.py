from datetime import datetime

from django.db import models


# Create your models here.

class HiringTranscript(models.Model):
    response_id = models.CharField(max_length=50)
    Candidate_id = models.CharField(max_length=50, null=True, blank=True)
    questionID = models.CharField(max_length=50, null=True, blank=True)
    video_type_id = models.IntegerField(default=0, null=True, blank=True)
    transcript = models.TextField()
    video_type = models.CharField(max_length=200, null=True, blank=True)
    total_words = models.IntegerField(default=0)
    stutter_count = models.IntegerField(default=0, null=True, blank=True)
    stutter_per_minute = models.DecimalField(max_digits=30, decimal_places=5, null=True, blank=True)
    Words_per_minute = models.DecimalField(max_digits=30, decimal_places=5, null=True, blank=True)
    average_confidence = models.DecimalField(max_digits=30, decimal_places=5, null=True, blank=True)
    speak_time = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    hurriness = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    grammar_error_count = models.IntegerField(default=0, null=True, blank=True)
    grammar_error_count_per_minute = models.DecimalField(max_digits=30, decimal_places=5, null=True, blank=True)

    def __str__(self):
        return str(self.response_id)


class HiringWord(models.Model):
    start_time = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    end_time = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    content = models.CharField(max_length=30, null=True, blank=True)
    pron = models.CharField(max_length=30, null=True, blank=True)
    confidence = models.DecimalField(max_digits=5, decimal_places=4, null=True, blank=True)
    mean_time = models.DecimalField(max_digits=30, decimal_places=5, null=True, blank=True)
    second = models.IntegerField(default=0)
    video_type = models.CharField(max_length=200, null=True, blank=True)
    transcript_id = models.ForeignKey(HiringTranscript, related_name="word_details", on_delete=models.CASCADE)
    is_stutter = models.BooleanField(default=False, null=True, blank=True)


class HiringErrorVideo(models.Model):
    video_url = models.TextField()
    error = models.TextField()
    error_date = models.DateTimeField(default=datetime.now, blank=True)


class HiringQuestionAnswer(models.Model):
    video_type = models.CharField(max_length=200, null=True, blank=True)
    video_type_id = models.IntegerField(default=0, null=True, blank=True)
    questionID = models.CharField(max_length=50, null=True, blank=True)
    question = models.CharField(max_length=1500, null=True, blank=True)
    answer = models.CharField(max_length=10000, null=True, blank=True)
    cleaned_answer = models.TextField(default='NA', null=True, blank=True)


class HiringRelevance(models.Model):
    transcript = models.TextField()
    Candidate_id = models.CharField(max_length=50, null=True, blank=True)
    questionID = models.CharField(max_length=50, null=True, blank=True)
    video_type_id = models.IntegerField(default=0, null=True, blank=True)
    video_type = models.CharField(max_length=200, null=True, blank=True)
    cleaned_transcript = models.TextField(default='NA', null=True, blank=True)


class HiringVideoIdToVideoTypeMaping(models.Model):
    video_type_id = models.IntegerField(default=0, null=True, blank=True)
    video_type = models.CharField(max_length=200, null=True, blank=True)


class HiringOkGrammerErrorList(models.Model):
    # error_id=models.AutoField()
    error_desc = models.CharField(max_length=3500, null=True, blank=True)


class HiringNotOkGrammerErrorList(models.Model):
    # error_id=models.AutoField()
    error_desc = models.CharField(max_length=3500, null=True, blank=True)


class HiringReiviewGrammerErrorList(models.Model):
    # error_id=models.AutoField()
    error_desc = models.CharField(max_length=3500, null=True, blank=True)

