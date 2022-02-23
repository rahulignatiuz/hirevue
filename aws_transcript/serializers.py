from rest_framework import serializers

from aws_transcript.models import HiringWord, HiringTranscript,HiringQuestionAnswer,HiringRelevance


class WordSerializer(serializers.ModelSerializer):
    # transcript_id = TranscriptSerializer()

    class Meta:
        model = HiringWord
        # fields = ("id", 'transcript_id', 'start_time', 'end_time', 'content', 'pron', 'confidence')
        fields = '__all__'


class TranscriptSerializer(serializers.ModelSerializer):
    word_details = WordSerializer(many=True)

    class Meta:
        model = HiringTranscript
        fields = '__all__'
        # fields = ("id", 'response_id', 'transcript', 'word_details', 'total_words', 'average_confidence', 'speak_time',
        #           'hurriness')


class RelevanceSerializer(serializers.ModelSerializer):

    class Meta:
        model = HiringRelevance
        fields = '__all__'
        # fields = ("id", 'response_id', 'transcript', 'word_details', 'total_words', 'average_confidence', 'speak_time',
        #           'hurriness')


class TranscriptEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = HiringTranscript
        fields = '__all__'

class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()

class SaveFileSerializer(serializers.Serializer):
    class Meta:
        model = HiringQuestionAnswer
        fields = "__all__"