from db.tweets import tweets as _tweets
from pyramid.view import view_config
import string
import re
import nltk
import simplejson as json

def sanitize(text):
    text = "".join([i for i in text if ord(i) in range(32, 127)])
    text = re.sub('http://','',text)
    text = re.sub(' +',' ',text)
    text = text.lower()
    return text

@view_config(renderer="index.pt", name="view")
def index_view(request): 
    return {}

@view_config(renderer="words.pt", name="words.json")
def index_view(request):
    t = _tweets('lisa.duffnet.local','csuser','password123%%%','chatterstats')
    results = t.getlast24hours()
    text = " ".join(results) 
    text = sanitize(text)
    _tokens = nltk.word_tokenize(text)
    tokens = nltk.FreqDist(word.lower() for word in _tokens)
    words = []
    for token,frequency in tokens.items():
        if len(token) > 3:
            word = []
            word.append(token)
            word.append(frequency)
            words.append(word)
    jsonwords = json.dumps(words)
    return { "jsonwords": jsonwords }
