from django.contrib import admin
# from hiring_aws_transcript.models import Transcript, Word, ErrorVideo
from hiring_aws_transcript.models import HiringTranscript, HiringWord, HiringErrorVideo,HiringQuestionAnswer,HiringRelevance,HiringVideoIdToVideoTypeMaping,HiringOkGrammerErrorList,HiringNotOkGrammerErrorList,HiringReiviewGrammerErrorList


class TranscriptAdmin(admin.ModelAdmin):
    list_display = (
    'response_id', 'transcript', 'total_words', 'video_type', 'average_confidence', 'speak_time', 'hurriness')

class WordAdmin(admin.ModelAdmin):
    list_display = (
    'transcript_id', 'start_time', 'end_time', 'content', 'pron', 'confidence', 'mean_time', 'second', 'video_type')


class ErrorVideoAdmin(admin.ModelAdmin):
    list_display = ('video_url', 'error', 'error_date')

class QuestionAnswerAdmin(admin.ModelAdmin):
    list_display = ('video_type','video_type_id','questionID','question','answer')


class RelevanceAdmin(admin.ModelAdmin):
    list_display = ('transcript','Candidate_id','questionID','video_type_id','video_type')

class VideoIdToVideoTypeMapingAdmin(admin.ModelAdmin):
    list_display = ('video_type_id','video_type')

# class HiringOkErrorListAdmin(admin.ModelAdmin):
#     list_display = ('error_desc')

# class HiringNotOkErrorListAdmin(admin.ModelAdmin):
#     list_display = ('error_desc')

# class HiringReiviewErrorListAdmin(admin.ModelAdmin):
#     list_display = ('error_desc')



admin.site.register(HiringTranscript, TranscriptAdmin)
admin.site.register(HiringWord, WordAdmin)
admin.site.register(HiringErrorVideo, ErrorVideoAdmin)
admin.site.register(HiringQuestionAnswer,QuestionAnswerAdmin)
admin.site.register(HiringRelevance,RelevanceAdmin)
admin.site.register(HiringVideoIdToVideoTypeMaping,VideoIdToVideoTypeMapingAdmin)
admin.site.register(HiringOkGrammerErrorList)
admin.site.register(HiringNotOkGrammerErrorList)
admin.site.register(HiringReiviewGrammerErrorList)