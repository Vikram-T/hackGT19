from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize, sent_tokenize
from .analyse import _run_article_summary
# import nltk
# nltk.download()


def upload(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        # sound = AudioSegment.from_mp3(uploaded_file)
        # sound.export('test.wav')
        fs = FileSystemStorage()
        fs.save(uploaded_file.name, uploaded_file)
        file = open('/Users/josh/simples/simples/crap.txt','r')
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
    pass

def results(request):
    return render(request, 'results.html', {'data':dict})
