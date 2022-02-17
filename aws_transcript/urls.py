from django.urls import include, path
from .views import AWSTranscribe, Transcribe, GetWord

urlpatterns = [
    path('aws/transcribe', AWSTranscribe.as_view()),
    path('transcribe', Transcribe.as_view()),
    path('word', GetWord.as_view()),
]
