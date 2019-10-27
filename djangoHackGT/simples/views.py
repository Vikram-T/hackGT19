from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize, sent_tokenize
from .analyse import _run_article_summary
from .AzureKeyWords import AzureKeyWords
import os
from .mp3totext import mp3totext

def home(request):
    return render(request, 'index.html')

def upload(request):
    if request.method == 'POST' and request.FILES['uploaded_file']:
        uploaded_file = request.FILES['uploaded_file']
        fh = open(settings.MEDIA_ROOT+"/"+uploaded_file.name, 'r')
        mp3Object = mp3totext(fh)
        fs = FileSystemStorage()
        filename = fs.save(uploaded_file.name, uploaded_file)
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"/Users/vikram/Documents/Programming/hackGT19/djangoHackGT/HackGT-77a8a0d36669.json"
        mp3Object.sample_long_running_recognize()

        uploaded_file_url = fs.url(filename)
        return render(request, 'simple_upload.html', {'uploaded_file_url': uploaded_file_url})
    return render(request, 'simple_upload.html')

# }

def gather_data(text):
    key_word = AzureKeyWords(text)
    r = key_word.splitAndSend('https://eastus.api.cognitive.microsoft.com/text/analytics/v2.1/keyPhrases',apiKey='af38334380c747b0873a35753787def2')
    print(r.status_code)
    key_notes_values = r.json()['documents'][0]['keyPhrases']
    file = open(text,'r')
    data = file.read().replace('\n', '')
    summary_text = (_run_article_summary(data)).split(' ')
    print(summary_text)
    print(key_notes_values)
    file.close()
    return {'text': data,'summary':summary_text ,'keywords': key_notes_values}


def results(request):
    dict = gather_data(r'/Users/vikram/Documents/Programming/hackGT19/djangoHackGT/media/gcpTestAudio.wav_transcript.txt')
    return render(request, 'results.html', {'data':dict})

