from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from sklearn import preprocessing
import pandas as pd
from hiring_aws_transcript.helper import aws_transcribe, get_stutter_info, get_cleaned_ans, get_cleaned_transcript, \
    check_grammer_error
from hiring_aws_transcript.models import HiringTranscript, HiringWord, HiringQuestionAnswer, HiringRelevance, \
    HiringVideoIdToVideoTypeMaping, HiringOkGrammerErrorList, HiringNotOkGrammerErrorList, HiringReiviewGrammerErrorList
from hiring_aws_transcript.serializers import TranscriptSerializer, WordSerializer, TranscriptEditSerializer, \
    FileUploadSerializer, RelevanceSerializer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.metrics.pairwise import linear_kernel
import pickle


class AWSTranscribe(APIView):
    def post(self, request, format=None):
        urls = request.data['url']
        video_type = request.data['video_type']
        transcribe_id, success_status = aws_transcribe(urls, video_type)

        if success_status == "Success":
            transcript_data = HiringTranscript.objects.filter(pk__in=transcribe_id)
            serializer = TranscriptSerializer(transcript_data, many=True)
            result = serializer.data
        else:
            result = "Some Error...."

        content = {
            "status": success_status,
            "result": result
        }
        return Response(content, status=status.HTTP_201_CREATED)


class Transcribe(generics.CreateAPIView):
    def get(self, request, *args, **kwargs):
        try:
            stutter_count = 0
            stutter = ['um', 'uh', 'Um', 'Uh', 'Mhm', 'Ah', 'hm', 'hmm', 'Hm', 'Hmm']
            transcript_data = HiringTranscript.objects.all()
            # tr_serializer = TranscriptEditSerializer(transcript_data, many=True)
            # word_data = Word.objects.all()
            # wr_serializer = WordSerializer(word_data, many=True)
            # df_tran=tr_serializer.data
            # df_word=wr_serializer.data
            # df_tran,df_word=get_stutter_info(df_tran,df_word)
            # label_encoder = preprocessing.LabelEncoder()
            # label_encoder.fit(df_tran['video_type'])
            # df_tran['video_type_id']= label_encoder.transform(df_tran['video_type'])
            for transcript in transcript_data:
                Candidate_id, questionID = transcript.response_id.split("_")

                words = HiringWord.objects.filter(transcript_id=transcript.id)
                for word in words:
                    if word.content in stutter:
                        word.is_stutter = True
                        stutter_count += 1
                        word.save()
                transcript.Words_per_minute = transcript.hurriness * 60
                transcript.Candidate_id = Candidate_id
                transcript.questionID = questionID
                transcript.stutter_count = stutter_count
                transcript.stutter_per_minute = stutter_count * 60 / transcript.speak_time
                transcript.save()

            content = {

                "result": 'success'
            }
        except Exception as e:
            content = {

                "result": str(e)
            }
        return Response(content, status=status.HTTP_201_CREATED)


# class UploadLexiconDataView(generics.CreateAPIView):
# serializer_class = FileUploadSerializer


# def post(self, request, *args, **kwargs):
# serializer = self.get_serializer(data=request.data)
# serializer.is_valid(raise_exception=True)
# file = serializer.validated_data['file']
# reader = pd.read_csv(file)
# for _, row in reader.iterrows():
# new_file = LexiconData(
# content=row['content'],
# sentiment=row['Sentiment'],
# score=row['SCORE']
# )
# new_file.save()
# return Response({"status": "success"}, status.HTTP_201_CREATED)


class import_question_and_data(generics.CreateAPIView):
    serializer_class = FileUploadSerializer

    def post(self, request, *args, **kwargs):
        # try:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        file = serializer.validated_data['file']
        df_question_ans = pd.read_excel(file, sheet_name='Sheet1')
        print(range(len(df_question_ans)))
        for ind, row in df_question_ans.iterrows():
            print(row['video_type'], row['video_type_id'], row['questionID'], row['question'], row['answer'])
            QA_data = HiringQuestionAnswer(video_type=row['video_type'], video_type_id=row['video_type_id'],
                                           questionID=row['questionID'], question=row['question'], answer=row['answer'])
            QA_data.save()
        content = {

            "result": 'success'
        }
        return Response(content, status=status.HTTP_201_CREATED)
        # except Exception as e:
        #     content = {

        #         "result":str(e)
        #     }
        #     return Response(content, status=status.HTTP_201_CREATED)


# class Transcribe(generics.CreateAPIView):
#     def get(self, request, *args, **kwargs):
#         transcript_data = Transcript.objects.all()
#         tr_serializer = TranscriptEditSerializer(transcript_data, many=True)
#         word_data = Word.objects.all()
#         wr_serializer = WordSerializer(word_data, many=True)
#         df_tran=tr_serializer.data
#         df_word=wr_serializer.data

# df_word = pd.json_normalize(df_word)
# df_tran = pd.json_normalize(df_tran)
# print(wr_serializer.data)
# return Response(wr_serializer.data, status.HTTP_201_CREATED)
# print(tr_serializer.data)
# return Response(tr_serializer.data, status.HTTP_201_CREATED)


# class GetWord(generics.CreateAPIView):
#     def get(self, request, *args, **kwargs):
# word_data = Word.objects.all()
# wr_serializer = WordSerializer(word_data, many=True)
# print(wr_serializer.data)
# return Response(wr_serializer.data, status.HTTP_201_CREATED)

class GetCleannedData(generics.CreateAPIView):
    def get(self, request, *args, **kwargs):
        qa_data = HiringQuestionAnswer.objects.all()
        resp = get_cleaned_ans(qa_data)
        content = {"result": resp}
        return Response(content, status.HTTP_201_CREATED)


class FillRelevanceTable(generics.CreateAPIView):
    def get(self, request, *args, **kwargs):
        transcript_datas = HiringTranscript.objects.all()
        corpus = []
        for transcript in transcript_datas:
            relven = HiringRelevance()
            relven.transcript = transcript.transcript
            relven.Candidate_id = transcript.Candidate_id
            relven.questionID = transcript.questionID
            relven.video_type = transcript.video_type
            relven.save()
            relven.video_type_id = HiringVideoIdToVideoTypeMaping.objects.get(
                video_type=transcript.video_type).video_type_id
            transcript.video_type_id = HiringVideoIdToVideoTypeMaping.objects.get(
                video_type=transcript.video_type).video_type_id
            transcript.save()
            relven.save()
            review = get_cleaned_transcript(relven)
            corpus.append(review)
        content = {'result': corpus}
        return Response(content, status.HTTP_201_CREATED)


class CreatePickelFile(generics.CreateAPIView):
    def get(self, request, *args, **kwargs):
        tfidfvectorizer = TfidfVectorizer(analyzer='word')
        QNA_data = HiringQuestionAnswer.objects.all()
        for QNA in QNA_data:
            cleaned_ans = [QNA.cleaned_answer]
            tfidfvectorizer.fit(cleaned_ans)
            picknm = 'answer' + str(QNA.id) + ".pkl"
            # answer3.pkl
            with open(picknm, 'wb') as files:
                pickle.dump(tfidfvectorizer, files)
        content = {'result': 'success'}
        return Response(content, status.HTTP_201_CREATED)


class CalculateCosineSimilarities(generics.CreateAPIView):
    def post(self, request, *args, **kwargs):
        # tfidfvectorizer = TfidfVectorizer(analyzer='word')
        questionID = request.data['questionID']
        video_type = request.data['video_type']

        QNA = HiringQuestionAnswer.objects.get(questionID=questionID, video_type=video_type)
        picknm = 'answer' + str(QNA.id) + ".pkl"
        print(picknm)
        with open(picknm, 'rb') as f:
            lr = pickle.load(f)

        cleaned_ans = [QNA.cleaned_answer]
        relevence = HiringRelevance.objects.filter(questionID=questionID, video_type=video_type)
        relevence_serializer = RelevanceSerializer(relevence, many=True)
        df_relevence = relevence_serializer.data
        df_relevence = pd.json_normalize(df_relevence)
        # print(df_relevence)
        # print('209 this line')
        # print(df_relevence['cleaned_transcript'])
        doc_vectors = lr.transform(cleaned_ans + list(df_relevence['cleaned_transcript']))
        # print('215 this line')
        # print(doc_vectors.shape)
        # print(doc_vectors)
        cosine_similarities = linear_kernel(doc_vectors[0:1], doc_vectors[1:]).flatten()
        df_relevence['cosine_score'] = cosine_similarities
        # print('217 this line')
        df_relevence['Percentile Rank'] = df_relevence.cosine_score.rank(pct=True)

        # print(df_relevence.head())
        # print(type(cleaned_transcipt))
        content = {'result': df_relevence}
        return Response(content, status.HTTP_201_CREATED)


class FillGrammerErrorList(generics.CreateAPIView):
    serializer_class = FileUploadSerializer

    def post(self, request, *args, **kwargs):
        # try:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        file = serializer.validated_data['file']
        ok_list_errors = pd.read_excel(file, sheet_name='ok_list', header=None)
        Not_ok_list_errors = pd.read_excel(file, sheet_name='not_ok_list', header=None)
        print(ok_list_errors.columns)
        for ind, row in ok_list_errors.iterrows():
            HOkList = HiringOkGrammerErrorList(error_desc=row[0])
            HOkList.save()
        for ind, row in Not_ok_list_errors.iterrows():
            HNotOkList = HiringNotOkGrammerErrorList(error_desc=row[0])
            HNotOkList.save()
        content = {'result': 'success'}
        return Response(content, status.HTTP_201_CREATED)

        # for ind,row in ok_list_errors.iterrows():


class checkGrammarErrrorForAllTranscript(generics.CreateAPIView):
    def get(self, request, *args, **kwargs):
        data = HiringTranscript.objects.all()
        check_grammer_error(data)
        content = {'result': 'success'}
        return Response(content, status.HTTP_201_CREATED)


class import_videoID_videoType(generics.CreateAPIView):
    serializer_class = FileUploadSerializer

    def post(self, request, *args, **kwargs):
        # try:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        file = serializer.validated_data['file']
        df_videoID_videoType = pd.read_excel(file, sheet_name='Sheet2',header=None)
        print(range(len(df_videoID_videoType)))
        for ind, row in df_videoID_videoType.iterrows():
            # print(row['video_type'], row['video_type_id'], row['questionID'], row['question'], row['answer'])
            # QA_data = HiringQuestionAnswer(video_type=row['video_type'], video_type_id=row['video_type_id'],
            #                                questionID=row['questionID'], question=row['question'], answer=row['answer'])
            # QA_data.save()
            HVIDVT=HiringVideoIdToVideoTypeMaping(video_type_id=row[1],video_type=row[0])
            HVIDVT.save()
        content = {

            "result": 'success'
        }
        return Response(content, status=status.HTTP_201_CREATED)











