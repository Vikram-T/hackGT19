from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize, sent_tokenize
from .analyse import _run_article_summary
from .AzureKeyWords import AzureKeyWords
# import nltk
# nltk.download()
import pprint

def home(request):
    return render(request, 'index.html')

def upload(request):
    if request.method == 'POST' and request.FILES['uploaded_file']:
        uploaded_file = request.FILES['uploaded_file']
        # sound = AudioSegment.from_mp3(uploaded_file)
        # sound.export('test.wav')
        fs = FileSystemStorage()
        filename = fs.save(uploaded_file.name, uploaded_file)
        uploaded_file_url = fs.url(filename)
        return render(request, 'simple_upload.html', {'uploaded_file_url': uploaded_file_url})
    return render(request, 'simple_upload.html')

# }

def gather_data(text):
    key_word = AzureKeyWords(text)
    r = key_word.splitAndSend('https://eastus.api.cognitive.microsoft.com/text/analytics/v2.1/keyPhrases',apiKey='af38334380c747b0873a35753787def2')
    print(r.status_code)
    key_notes_values = r.json()['documents'][0]['keyPhrases']
    file = open('/Users/josh/hackGT19/djangoHackGT/media/algo.txt','r')
    data = file.read().replace('\n', '')
    summary_text = (_run_article_summary(data)).split(' ')
    print(summary_text)
    print(key_notes_values)
    file.close()
    return {'text': data,'summary':summary_text ,'keywords': key_notes_values}


def results(request):
    dict = gather_data('/Users/josh/hackGT19/djangoHackGT/media/algo.txt')
    return render(request, 'results.html', {'data':dict})
