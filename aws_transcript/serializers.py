from rest_framework import serializers

from aws_transcript.models import Word, Transcript


class WordSerializer(serializers.ModelSerializer):
    # transcript_id = TranscriptSerializer()

    class Meta:
        model = Word
        # fields = ("id", 'transcript_id', 'start_time', 'end_time', 'content', 'pron', 'confidence')
        fields = '__all__'


class TranscriptSerializer(serializers.ModelSerializer):
    word_details = WordSerializer(many=True)

    class Meta:
        model = Transcript
        # fields = '__all__'
        fields = ("id", 'response_id', 'transcript', 'word_details', 'total_words', 'average_confidence', 'speak_time',
                  'hurriness')


class TranscriptEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transcript
        fields = '__all__'
