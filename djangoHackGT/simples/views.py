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


def upload(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        # sound = AudioSegment.from_mp3(uploaded_file)
        # sound.export('test.wav')
        fs = FileSystemStorage()
        fs.save(uploaded_file.name, uploaded_file)
        file = open('/Users/josh/hackGT19/djangoHackGT/simples/crap.txt','r')
        data = file.read().replace('\n', '')
        answer = _run_article_summary(data)
        print(answer)
    return render(request, 'index.html')


dict = {
    'text': ['Once', 'upon', 'a', 'time', 'in', 'a', 'land', 'far', 'far', 'away', 'there', 'was', 'a', 'guy', 'who', 'lived', 'in', 'a', 'huge', 'castle'],
    'keywords': ['Once', 'time'],
    'complex':['time', 'far', 'was'],
}

def gather_data(text):
    key_word = AzureKeyWords(text)
    r = key_word.splitAndSend('https://eastus.api.cognitive.microsoft.com/text/analytics/v2.1/keyPhrases',apiKey='af38334380c747b0873a35753787def2')
    print(r.status_code)
    key_notes_values = r.json()['documents'][0]['keyPhrases']
    file = open('/Users/josh/hackGT19/djangoHackGT/simples/crap.txt','r')
    data = file.read().replace('\n', '')
    summary_text = _run_article_summary(data)
    file.close()


def results(request):
    gather_data('/Users/josh/hackGT19/djangoHackGT/simples/crap.txt')
    return render(request, 'results.html', {'data':dict})
