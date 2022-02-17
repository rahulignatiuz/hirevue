from datetime import datetime

from django.db import models


# Create your models here.

class Transcript(models.Model):
    response_id = models.CharField(max_length=50)
    transcript = models.TextField()
    video_type = models.CharField(max_length=200, null=True, blank=True)
    total_words = models.IntegerField(default=0)
    average_confidence = models.DecimalField(max_digits=30, decimal_places=5, null=True, blank=True)
    speak_time = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    hurriness = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return str(self.response_id)


class Word(models.Model):
    start_time = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    end_time = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    content = models.CharField(max_length=30, null=True, blank=True)
    pron = models.CharField(max_length=30, null=True, blank=True)
    confidence = models.DecimalField(max_digits=5, decimal_places=4, null=True, blank=True)
    mean_time = models.DecimalField(max_digits=30, decimal_places=5, null=True, blank=True)
    second = models.IntegerField(default=0)
    video_type = models.CharField(max_length=200, null=True, blank=True)
    transcript_id = models.ForeignKey(Transcript, related_name="word_details", on_delete=models.CASCADE)


class ErrorVideo(models.Model):
    video_url = models.TextField()
    error = models.TextField()
    error_date = models.DateTimeField(default=datetime.now, blank=True)
