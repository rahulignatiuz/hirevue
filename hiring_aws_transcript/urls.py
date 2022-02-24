from django.urls import include, path
from .views import AWSTranscribe, Transcribe,import_question_and_data,GetCleannedData,FillRelevanceTable,CreatePickelFile,CalculateCosineSimilarities,FillGrammerErrorList,checkGrammarErrrorForAllTranscript,import_videoID_videoType
urlpatterns = [
    path('aws/transcribe', AWSTranscribe.as_view()),
    path('transcribe', Transcribe.as_view()),
    path('ImpQA', import_question_and_data.as_view()),
    path('GetCleannedData', GetCleannedData.as_view()),
    path('FillRelevanceTable', FillRelevanceTable.as_view()),
    path('CreatePickelFile', CreatePickelFile.as_view()),
    path('CalculateCosineSimilarities', CalculateCosineSimilarities.as_view()),
    path('FillGrammerErrorList', FillGrammerErrorList.as_view()),
    path('checkGrammarErrrorForAllTranscript', checkGrammarErrrorForAllTranscript.as_view()),
    path('import_videoID_videoType', import_videoID_videoType.as_view()),
    # path('word', GetWord.as_view()),
]