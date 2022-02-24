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
from hiring_aws_transcript.models import HiringTranscript, HiringWord, HiringErrorVideo,HiringOkGrammerErrorList,HiringNotOkGrammerErrorList,HiringReiviewGrammerErrorList,HiringVideoIdToVideoTypeMaping
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer
from sklearn import preprocessing
from sklearn.metrics.pairwise import linear_kernel
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import HashingVectorizer
import language_tool_python



def aws_transcribe(urls, video_type):
    success_status = "Success"
    transcribe_id = []
    stutter_count=0
    stutter = ['um' , 'uh' , 'Um' , 'Uh' , 'Mhm' , 'Ah', 'hm' , 'hmm' , 'Hm' , 'Hmm' ] 
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
                    transcript = HiringTranscript()
                    transcript.transcript = result['results']['transcripts'][0]['transcript']
                    transcript.response_id = response_id
                    transcript.video_type = video_type
                    transcript.save()
                    Candidate_id,questionID=transcript.response_id.split("_")
                    transcribe_id.append(transcript.id)
                    items = result['results']['items']
                    for item in items:
                        content = item['alternatives'][0]['content']
                        word = HiringWord()
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
                    words=HiringWord.objects.filter(transcript_id=transcript.id)
                    for word in words:
                        if word.content in stutter:
                            word.is_stutter=True
                            stutter_count+=1
                            word.save()
                    speak_time = max(end) - min(start)
                    hurriness = len(total_words) / speak_time
                    stutter_per_minute=stutter_count*60/(speak_time)
                    HiringTranscript.objects.filter(pk=transcript.id).update(
                        average_confidence=statistics.mean(average_confidence),
                        total_words=len(total_words), speak_time=speak_time, hurriness=hurriness,Words_per_minute=hurriness*60,stutter_count=stutter_count,stutter_per_minute=stutter_per_minute,Candidate_id=Candidate_id,questionID=questionID)
                    transcript.video_type_id=HiringVideoIdToVideoTypeMaping.objects.get(video_type=transcript.video_type).video_type_id
                    transcript.save()
                    check_grammer_error([transcript])
                else:
                    success_status = "Failure"
            else:
                success_status = "Failure"
        except Exception as e:
            error_video_insert = HiringErrorVideo()
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
            # delete_s3(url)
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




def get_stutter_info(df_tran, df_word):
    df_word = pd.json_normalize(df_word)
    df_tran = pd.json_normalize(df_tran)
    df_tran[[ "Candidate_id", "questionID"]] = df_tran["response_id"].str.split(pat="_", expand=True)

    label_encoder = preprocessing.LabelEncoder()

    df_tran['video_type']= label_encoder.fit_transform(df_tran['video_type'])

    df_tran.dropna(inplace = True)

    # Stutter module

    stutter = ['um' , 'uh' , 'Um' , 'Uh' , 'Mhm' , 'Ah', 'hm' , 'hmm' , 'Hm' , 'Hmm' ] 

    df_word['is_stutter'] = df_word['content'].isin(stutter)

    unique_vid = df_word.transcript_id.unique()

    df_word['is_stutter'] = df_word['is_stutter'].astype(int)

    stutter_count = []

    for k in range(0 , len(unique_vid)):
        df_temp = df_word[df_word['transcript_id'] ==unique_vid[k]].copy()
        df_temp.reset_index(inplace = True)
        temp_stutter_count = 0
        for j in range(0, len(df_temp)):
            if df_temp['is_stutter'][j] == 1:
                temp_stutter_count =temp_stutter_count+1
                
        stutter_count.append(temp_stutter_count)  
        
    df_tran['stutter_count'] = stutter_count

    df_tran['speak_time'] = df_tran['speak_time'].astype(float)

    df_tran['stutter_per_minute'] = (df_tran['stutter_count']* 60)/df_tran['speak_time']

    # Speed module

    df_tran['hurriness'] = df_tran['hurriness'].astype(float)

    df_tran['Words_per_minute']= df_tran['hurriness']*60


    
    return df_tran,df_word



def get_cleaned_ans(data):
    ps = PorterStemmer()
    wordnet=WordNetLemmatizer()
    review = []
    corpus = []
    for i in data:
        review = re.sub('[^a-zA-Z]', ' ',i.answer )
        review = review.lower()
        review = review.split()
        review = [wordnet.lemmatize(word) for word in review if not word in set(stopwords.words('english'))]
        #review = [ps.stem(word) for word in review if not word in set(stopwords.words('english'))]
        #review = [wordnet.lemmatize(word) for word in review ]
        review = ' '.join(review)
        corpus.append(review)
        i.cleaned_answer=review
        i.save()
    return corpus

def get_cleaned_transcript(data):
    ps = PorterStemmer()
    wordnet=WordNetLemmatizer()
    review = []
    corpus = []
    # for i in range(len(data)):
    review = re.sub('[^a-zA-Z]', ' ',data.transcript )
    review = review.lower()
    review = review.split()
    review = [wordnet.lemmatize(word) for word in review if not word in set(stopwords.words('english'))]
    #review = [ps.stem(word) for word in review if not word in set(stopwords.words('english'))]
    #review = [wordnet.lemmatize(word) for word in review ]
    review = ' '.join(review)
    data.cleaned_transcript=review
    data.save()
        # corpus.append(review)
    return review


def check_grammer_error(data):
    tl = language_tool_python.LanguageTool('en-US')
    # print(not_ok_list)
    
    for i in data:
        count=0
        match = tl.check(i.transcript)
        # print(match)
        # print('------------------------------')
        # print(match[0])
        # print('------------------------------')
        # print(match[0].message)
        # print('------------------------------')
        # HiringOkGrammerErrorList.objects.filter(error_desc=)
        if match==[]:
            pass
        else:

            if not HiringNotOkGrammerErrorList.objects.filter(error_desc=match[0].message).exists() :
                if HiringOkGrammerErrorList.objects.filter(error_desc=match[0].message).exists():
                    count+=1
                else:
                    hRievew=HiringReiviewGrammerErrorList(error_desc=match[0].message)
                    hRievew.save()
        i.grammar_error_count=count
        i.grammar_error_count_per_minute=count*60/i.speak_time
        i.save()
