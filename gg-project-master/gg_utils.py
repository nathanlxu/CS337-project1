import json
import sys
import nltk
import string
from nltk.tokenize import RegexpTokenizer
from nltk.tokenize import word_tokenize

official_tweets = []
tweets = []

def get_tweets(year, tokenize=True):
	#change this to read desired file
	filename = 'gg jsons/gg%s.json' % str(year)
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
		text.append(t)

	# returns text of tweets if 'tokenize' is false
	if not tokenize:
		return text

	tokenizer = RegexpTokenizer(r'\w+')

	for tweet in text:
		tweets.append(nltk.wordpunct_tokenize(tweet))

	return tweets

def get_award_keywords(award_titles, stopwords):
	award_mapping = {}
	for award in award_titles:
		key_words = []
		award_tokens = word_tokenize(award)
		for words in award_tokens:
			if words not in stopwords:
				key_words.append(words)

		award_mapping[award] = key_words

	return award_mapping

# print(get_tweets(2013, tokenize=False)[:3])