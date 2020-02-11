import json
import sys
import nltk
import string
from random import sample
from nltk.tokenize import RegexpTokenizer
from nltk.tokenize import word_tokenize

official_tweets = []
tweets = []
MAX_LENGTH = 5000


def get_tweets(year, tokenize=True):
    # change this to read desired file
    filename = 'gg jsons/gg%s.json' % str(year)
    text = []
    try:
        # the gg2013 and 2015 format is one giant json file
        with open(filename) as json_file:
            jsonData = json.load(json_file)
    except:
        # gg2020 is one json object per line
        jsonData = []
        with open(filename, encoding="utf-8") as f:
            for line in f:
                jsonData.append(json.loads(line))

    for item in jsonData:
        t = item.get("text")
        text.append(t)

    print("GOT DATA OF LENGTH", len(text))
    if len(text) > MAX_LENGTH:
        sampled_text = sample(text, MAX_LENGTH)
    else:
        sampled_text = text

    # returns text of tweets if 'tokenize' is false
    if not tokenize:
        return sampled_text

    tokenizer = RegexpTokenizer(r'\w+')

    for tweet in sampled_text:
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


def partition(pred, iterable):
    trues = []
    falses = []
    for item in iterable:
        if pred(item):
            trues.append(item)
        else:
            falses.append(item)
    return trues, falses

def filter_tweets(tweets, keywords):
    return [tweet for tweet in tweets if any(keyword in tweet for keyword in keywords)]

# print(get_tweets(2013, tokenize=False)[:3])
