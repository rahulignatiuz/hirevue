from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from aws_transcript.helper import aws_transcribe
from aws_transcript.models import Transcript, Word
from aws_transcript.serializers import TranscriptSerializer, WordSerializer, TranscriptEditSerializer


class AWSTranscribe(APIView):
    def post(self, request, format=None):
        urls = request.data['url']
        video_type = request.data['video_type']
        transcribe_id, success_status = aws_transcribe(urls, video_type)

        if success_status == "Success":
            transcript_data = Transcript.objects.filter(pk__in=transcribe_id)
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
        transcript_data = Transcript.objects.all()
        tr_serializer = TranscriptEditSerializer(transcript_data, many=True)
        print(tr_serializer.data)
        return Response(tr_serializer.data, status.HTTP_201_CREATED)


class GetWord(generics.CreateAPIView):
    def get(self, request, *args, **kwargs):
        word_data = Word.objects.all()
        wr_serializer = WordSerializer(word_data, many=True)
        print(wr_serializer.data)
        return Response(wr_serializer.data, status.HTTP_201_CREATED)
