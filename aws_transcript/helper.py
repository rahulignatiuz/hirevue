import os
import boto3
import urllib
import json
import random
import string
import time
import math
import moviepy.video.io.ffmpeg_tools
import statistics
from moviepy.editor import *
from botocore.exceptions import NoCredentialsError
from django.conf import settings
from aws_transcript.models import Transcript, Word, ErrorVideo


def aws_transcribe(urls, video_type):
    success_status = "Success"
    transcribe_id = []
    for url in urls:
        average_confidence = []
        total_words = []
        number_of_dot = []
        start = []
        end = []
        print(url)
        try:
            s3_url = upload_file_s3(url)
            if s3_url:
                job = url.rsplit('/', 2)
                response_id = job[-2] + "_" + os.path.splitext(job[-1])[0]
                # response_id = os.path.basename(url)
                result = speech_to_text(s3_url)
                if result:
                    success_status = "Success"
                    transcript = Transcript()
                    transcript.transcript = result['results']['transcripts'][0]['transcript']
                    transcript.response_id = response_id
                    transcript.video_type = video_type
                    transcript.save()
                    transcribe_id.append(transcript.id)
                    items = result['results']['items']
                    for item in items:
                        content = item['alternatives'][0]['content']
                        word = Word()
                        word.transcript_id = transcript
                        word.pron = item['type']
                        word.content = content
                        word.video_type = video_type
                        if item['type'] == "pronunciation":
                            word.confidence = float(item['alternatives'][0]['confidence'])
                            mean_time = (float(item['start_time']) + float(item['end_time'])) / 2
                            word.start_time = float(item['start_time'])
                            word.end_time = float(item['end_time'])
                            word.mean_time = mean_time
                            word.second = math.ceil(mean_time)
                            average_confidence.append(float(item['alternatives'][0]['confidence']))
                            total_words.append(item['alternatives'][0]['content'])
                            start.append(float(item['start_time']))
                            end.append(float(item['end_time']))
                        else:
                            if item['alternatives'][0]['content'] == ".":
                                number_of_dot.append(item['alternatives'][0]['content'])
                        word.save()
                    speak_time = max(end) - min(start)
                    hurriness = len(total_words) / speak_time
                    Transcript.objects.filter(pk=transcript.id).update(
                        average_confidence=statistics.mean(average_confidence),
                        total_words=len(total_words), speak_time=speak_time, hurriness=hurriness)
                else:
                    success_status = "Failure"
            else:
                success_status = "Failure"
        except Exception as e:
            error_video_insert = ErrorVideo()
            error_video_insert.video_url = url
            error_video_insert.error = e
            error_video_insert.save()
            continue
    return transcribe_id, success_status


def speech_to_text(url):
    aws_access_key_id = settings.AWS_ACCESS_KEY_ID
    aws_secret_access_key = settings.AWS_SECRET_ACCESS_KEY
    job_name = get_random_text()
    job_uri = "https://webtalkxscript.s3.amazonaws.com/" + url
    transcribe = boto3.client('transcribe', aws_access_key_id=aws_access_key_id,
                              aws_secret_access_key=aws_secret_access_key, region_name='us-east-1')
    try:
        transcribe.start_transcription_job(TranscriptionJobName=job_name, Media={'MediaFileUri': job_uri},
                                           MediaFormat='mp3', LanguageCode='en-US')
        while True:
            status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
            if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
                break
            print("Not ready yet...")
            time.sleep(2)
        print(status)

        if status['TranscriptionJob']['TranscriptionJobStatus'] == 'COMPLETED':
            response = urllib.request.urlopen(status['TranscriptionJob']['Transcript']['TranscriptFileUri'])
            delete_s3(url)
            speech = json.loads(response.read())
        return speech
    except Exception as e:
        print("++++++++++e++++", e)
        return False


def upload_file_s3(url):
    file_name = get_random_text() + ".mp3"
    download_path = "media/" + file_name
    upload_path = "samples/" + file_name
    # urllib.request.urlretrieve(url, download_path)
    moviepy.video.io.ffmpeg_tools.ffmpeg_extract_audio(url, download_path)
    s3, bucket_name = s3_connection()
    try:
        s3.upload_file(download_path, bucket_name, upload_path)
        pull_upload_path = upload_path
        print("Upload Successful")
        if os.path.exists(download_path):
            os.remove(download_path)
        else:
            print("The file does not exist")
        return pull_upload_path
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False


def get_random_text():
    char_set = string.ascii_uppercase + string.digits
    random_text = ''.join(random.sample(char_set * 6, 6))
    return random_text


def delete_s3(file_name):
    s3, bucket_name = s3_connection()
    s3.delete_object(Bucket=bucket_name, Key=file_name)


def s3_connection():
    bucket_name = 'webtalkxscript'
    aws_access_key_id = settings.AWS_ACCESS_KEY_ID
    aws_secret_access_key = settings.AWS_SECRET_ACCESS_KEY
    s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
    return s3, bucket_name
