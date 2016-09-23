from HTMLParser import HTMLParser
import cPickle as pickle
import re #Regex
import string
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

postagger   = pickle.load(open("..\POSTAGGER.p", "rb"))
stopword_html = open("..\id.stopwords.01.01.2016.txt",'r').read()
stopwords     = stopword_html.split("\n")

def onlyAZ(teks):
	return re.sub(r'[^a-zA-Z]',' ', teks)

def onlyNVFromSentence(teks):
	splitted = postagger.tag(onlyAZ(teks).split())
	nouns = [word for word,pos in splitted \
		if (pos == 'NN' or pos == 'NNP' or 
			pos == 'NNS' or pos == 'VB')]
	nounsSentence = string.join(nouns)
	return nounsSentence

class MLStripper(HTMLParser):
	def __init__(self):
		self.reset()
		self.fed = []
	def handle_data(self, d):
		self.fed.append(d)
	def get_data(self):
		return ' '.join(self.fed)

def strip_tags(html):
	s = MLStripper()
	s.feed(html)
	striped  = s.get_data()                         #get HTML-Tags free text
	onlyaz   = onlyAZ(striped)
	lowers   = onlyaz.lower()                      #Lowercase all words
	nospace  = lowers.strip()                       #Remove leading and trailing white space
	return nospace

def posTag(par):
	par         = strip_tags(par)
	splittedPar = par.split('.')
	NVPar    	= ' '.join([onlyNVFromSentence(i) for i in splittedPar])
	return  NVPar

def rmStem(pars):
	factory = StemmerFactory()
	stripped= strip_tags(pars)
	stemmer = factory.create_stemmer()
	clean   = stemmer.stem(str(stripped)) #Stemming
	return clean