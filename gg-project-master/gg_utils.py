import json
import nltk
from copy import deepcopy
from nltk.tokenize import RegexpTokenizer
from nltk.tokenize import word_tokenize


def to_lower_case(text):
    text = deepcopy(text)
    return [t.lower() for t in text]


def get_tweets(year):
    filename = 'gg jsons/gg%s.json' % str(year)
    text = []
    try:
        # 2013 and 2015 format is one giant json file
        with open(filename) as json_file:
            tweets = json.load(json_file)
            for tweet in tweets:
                text.append(tweet["text"])
    except:
        # 2020 format is one json object per line
        with open(filename, encoding="utf-8") as f:
            for line in f:
                text.append(json.loads(line)["text"])

    return text


def filter_tweets(tweets, strict_keywords, loose_keywords, filterwords):
    return [tweet for tweet in tweets if all(keyword in tweet.lower() for keyword in strict_keywords)
            and any(keyword in tweet.lower() for keyword in loose_keywords)
            and not any(filterword in tweet.lower() for filterword in filterwords)]


def get_sample(tweets, max_len):
    print("DATA EXCEEDED MAX LENGTH OF", max_len, " - CREATING SAMPLE...")
    sub_samples = 10
    sample = []
    step_size = int(len(tweets) / sub_samples)
    sub_sample_size = int(max_len / sub_samples)
    for i in range(0, len(tweets), step_size):
        sample += tweets[i:i + sub_sample_size]
    print("CREATED SAMPLE OF LENGTH", len(sample))
    return sample


def get_tokenized_tweets(year, tokenize=True):
    MAX_LENGTH = 10000
    sub_samples = 10
    # change this to read desired file
    filename = 'gg jsons/gg%s.json' % str(year)
    text = []
    tweets = []
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
