from django.contrib import admin
from aws_transcript.models import Transcript, Word, ErrorVideo


# Register your models here.


class TranscriptAdmin(admin.ModelAdmin):
    list_display = (
    'response_id', 'transcript', 'total_words', 'video_type', 'average_confidence', 'speak_time', 'hurriness')


class WordAdmin(admin.ModelAdmin):
    list_display = (
    'transcript_id', 'start_time', 'end_time', 'content', 'pron', 'confidence', 'mean_time', 'second', 'video_type')


class ErrorVideoAdmin(admin.ModelAdmin):
    list_display = ('video_url', 'error', 'error_date')


admin.site.register(Transcript, TranscriptAdmin)
admin.site.register(Word, WordAdmin)
admin.site.register(ErrorVideo, ErrorVideoAdmin)
