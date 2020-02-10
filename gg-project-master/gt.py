import json
import sys
import nltk
import string
from nltk.tokenize import RegexpTokenizer

official_tweets = []

tweets = []

def get_tweets(year):

	#change this to read desired file
	filename = 'gg%s.json' % str(year)


	text = []
	try:
		#the gg2013 and 2015 format is one giant json file
		with open(filename) as json_file:
			jsonData = json.load(json_file)
	except:
		#gg2020 is one json object per line
		jsonData = []
		for line in open(filename, 'r'):
			jsonData.append(json.loads(line))

	for item in jsonData:
		t = item.get("text")
		text.append(t.lower())


	tokenizer = RegexpTokenizer(r'\w+')

	for tweet in text:
		tweets.append(nltk.wordpunct_tokenize(tweet))

	return tweets