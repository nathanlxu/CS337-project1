import json
import sys
import nltk
import string
from random import sample
from nltk.tokenize import RegexpTokenizer
from nltk.tokenize import word_tokenize

official_tweets = []
tweets = []
MAX_LENGTH = 10000
sub_samples = 10

def get_sample(tweets, max_len):
    print("CREATING SAMPLE")
    sample = []
    step_size = int(len(tweets)/sub_samples)
    sub_sample_size = int(max_len/sub_samples)
    for i in range(0, len(tweets), step_size):
        sample += tweets[i:i+sub_sample_size]
    print("CREATED SAMPLE OF LENGTH", len(sample))
    return sample

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
    # if len(tweets) / sub_samples > MAX_LENGTH:
    if len(text) / sub_samples > MAX_LENGTH:
        sampled_text = get_sample(text, MAX_LENGTH)
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

def filter_tweets(tweets, keywords, stopwords):
    return [tweet for tweet in tweets if any(keyword in tweet for keyword in keywords)
            and not any(stopword in tweet for stopword in stopwords)]
