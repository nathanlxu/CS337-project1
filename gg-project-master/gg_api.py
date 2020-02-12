'''Version 0.35'''
import sys
import re
import nltk
import spacy
from collections import Counter
from gg_utils import *
from random import sample
from collections import OrderedDict
from difflib import SequenceMatcher

OFFICIAL_AWARDS_1315 = ['cecil b. demille award', 'best motion picture - drama',
                        'best performance by an actress in a motion picture - drama',
                        'best performance by an actor in a motion picture - drama',
                        'best motion picture - comedy or musical',
                        'best performance by an actress in a motion picture - comedy or musical',
                        'best performance by an actor in a motion picture - comedy or musical',
                        'best animated feature film', 'best foreign language film',
                        'best performance by an actress in a supporting role in a motion picture',
                        'best performance by an actor in a supporting role in a motion picture',
                        'best director - motion picture', 'best screenplay - motion picture',
                        'best original score - motion picture', 'best original song - motion picture',
                        'best television series - drama',
                        'best performance by an actress in a television series - drama',
                        'best performance by an actor in a television series - drama',
                        'best television series - comedy or musical',
                        'best performance by an actress in a television series - comedy or musical',
                        'best performance by an actor in a television series - comedy or musical',
                        'best mini-series or motion picture made for television',
                        'best performance by an actress in a mini-series or motion picture made for television',
                        'best performance by an actor in a mini-series or motion picture made for television',
                        'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television',
                        'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television']

OFFICIAL_AWARDS_1819 = ['best motion picture - drama', 'best motion picture - musical or comedy',
                        'best performance by an actress in a motion picture - drama',
                        'best performance by an actor in a motion picture - drama',
                        'best performance by an actress in a motion picture - musical or comedy',
                        'best performance by an actor in a motion picture - musical or comedy',
                        'best performance by an actress in a supporting role in any motion picture',
                        'best performance by an actor in a supporting role in any motion picture',
                        'best director - motion picture', 'best screenplay - motion picture',
                        'best motion picture - animated', 'best motion picture - foreign language',
                        'best original score - motion picture', 'best original song - motion picture',
                        'best television series - drama', 'best television series - musical or comedy',
                        'best television limited series or motion picture made for television',
                        'best performance by an actress in a limited series or a motion picture made for television',
                        'best performance by an actor in a limited series or a motion picture made for television',
                        'best performance by an actress in a television series - drama',
                        'best performance by an actor in a television series - drama',
                        'best performance by an actress in a television series - musical or comedy',
                        'best performance by an actor in a television series - musical or comedy',
                        'best performance by an actress in a supporting role in a series, limited series or motion picture made for television',
                        'best performance by an actor in a supporting role in a series, limited series or motion picture made for television',
                        'cecil b. demille award']

filter_dict_1819 = {'best motion picture - drama':[['drama'],['motion','picture'],['actor','actress','television','tv','series']],
                   'best motion picture - musical or comedy':[['picture'],['musical','comedy'],['actor','actress','television','tv','series']],
                   'best performance by an actress in a motion picture - drama':[['actress','drama'],['motion','picture'],['television','tv','series']],
                   'best performance by an actor in a motion picture - drama':[['actor','drama'],['motion','picture'],['television','tv','series']],
                   'best performance by an actress in a motion picture - musical or comedy':[['actress','picture'],['musical','comedy'],['television','tv','series']],
                   'best performance by an actor in a motion picture - musical or comedy':[['actor','picture'],['musical','comedy'],['television','tv','series']],
                   'best performance by an actress in a supporting role in any motion picture':[['actress','supporting'],['motion','picture'],['television','tv','series']],
                   'best performance by an actor in a supporting role in any motion picture':[['actor','supporting'],['motion','picture'],['television','tv','series']],
                   'best director - motion picture':[['director'],['motion','picture'],['actor','actress','television','tv','series']],
                   'best screenplay - motion picture':[['screenplay'],['motion','picture'],['actor','actress','television','tv','series']],
                   'best motion picture - animated':[['animated'],['motion','picture','feature','film'],['actor','actress','television','tv','series']],
                   'best motion picture - foreign language':[['foreign'],['motion','picture','film'],['actor','actress','television','tv','series']],
                   'best original score - motion picture':[['score'],['motion','picture','film','movie'],['actor','actress','television','tv','series']],
                   'best original song - motion picture':[['song'],['motion','picture','film','movie'],['actor','actress','television','tv','series']],
                   'best television series - drama':[['drama'],['television','tv','series'],['actor','actress','motion picture']],
                   'best television series - musical or comedy':[['comedy'],['television','tv','series'],['actor','actress','motion picture']],
                   'best television limited series or motion picture made for television':[['picture','television'],['motion','picture','television','limited','series'],['actor','actress']],
                   'best performance by an actress in a limited series or a motion picture made for television':[['actress','picture','television'],['motion','picture','television','limited','series'],[]],
                   'best performance by an actor in a limited series or a motion picture made for television':[['actor','picture','television'],['motion','picture','television','limited','series'],[]],
                   'best performance by an actress in a television series - drama':[['actress','drama'],['television','tv','series'],['motion','picture']],
                   'best performance by an actor in a television series - drama':[['actor','drama'],['television','tv','series'],['motion','picture']],
                   'best performance by an actress in a television series - musical or comedy':[['actress','comedy'],['television','tv','series'],['motion','picture']],
                   'best performance by an actor in a television series - musical or comedy':[['actor','drama'],['television','tv','series'],['motion','picture']],
                   'best performance by an actress in a supporting role in a series, limited series or motion picture made for television':[['actress','supporting','picture','television'],['motion','picture','television','limited','series'],[]],
                   'best performance by an actor in a supporting role in a series, limited series or motion picture made for television':[['actor','supporting','picture','television'],['motion','picture','television','limited','series'],[]],
                   'cecil b. demille award':[[],['cecil','demille'],[]]}

filter_dict_1315 = {'best motion picture - drama':[['drama'],['motion','picture'],['actor','actress','television','tv','series']],
                   'best motion picture - comedy or musical':[['picture'],['musical','comedy'],['actor','actress','television','tv','series']],
                   'best performance by an actress in a motion picture - drama':[['actress','drama'],['motion','picture'],['television','tv','series']],
                   'best performance by an actor in a motion picture - drama':[['actor','drama'],['motion','picture'],['television','tv','series']],
                   'best performance by an actress in a motion picture - comedy or musical':[['actress','picture'],['musical','comedy'],['television','tv','series']],
                   'best performance by an actor in a motion picture - comedy or musical':[['actor','picture'],['musical','comedy'],['television','tv','series']],
                   'best performance by an actress in a supporting role in a motion picture':[['actress','supporting'],['motion','picture'],['television','tv','series']],
                   'best performance by an actor in a supporting role in a motion picture':[['actor','supporting'],['motion','picture'],['television','tv','series']],
                   'best director - motion picture':[['director'],['motion','picture'],['actor','actress','television','tv','series']],
                   'best screenplay - motion picture':[['screenplay'],['motion','picture'],['actor','actress','television','tv','series']],
                   'best animated feature film':[['animated'],['motion','picture','feature','film'],['actor','actress','television','tv','series']],
                   'best foreign language film':[['foreign'],['motion','picture','film'],['actor','actress','television','tv','series']],
                   'best original score - motion picture':[['score'],['motion','picture','film','movie'],['actor','actress','television','tv','series']],
                   'best original song - motion picture':[['song'],['motion','picture','film','movie'],['actor','actress','television','tv','series']],
                   'best television series - drama':[['drama'],['television','tv','series'],['actor','actress','motion picture']],
                   'best television series - comedy or musical':[['comedy'],['television','tv','series'],['actor','actress','motion picture']],
                   'best television mini-series or motion picture made for television':[['picture','television'],['motion','picture','television','limited','series'],['actor','actress']],
                   'best performance by an actress in a mini-series or a motion picture made for television':[['actress','picture','television'],['motion','picture','television'],[]],
                   'best performance by an actor in a mini-series or a motion picture made for television':[['actor','picture','television'],['motion','picture','television'],[]],
                   'best performance by an actress in a television series - drama':[['actress','drama'],['television','tv','series'],['motion','picture']],
                   'best performance by an actor in a television series - drama':[['actor','drama'],['television','tv','series'],['motion','picture']],
                   'best performance by an actress in a television series - comedy or musical':[['actress','comedy'],['television','tv','series'],['motion','picture']],
                   'best performance by an actor in a television series - comedy or musical':[['actor','drama'],['television','tv','series'],['motion','picture']],
                   'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television':[['actress','supporting','picture','television'],['motion','picture','television','limited','series'],[]],
                   'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television':[['actor','supporting','picture','television'],['motion','picture','television','limited','series'],[]],
                   'cecil b. demille award':[[],['cecil','demille'],[]]}

nltk.download('stopwords')
stopwords = nltk.corpus.stopwords.words('english')
additional_stopwords = ['/', '://', 'am', 'and', 'award', 'awards', 'awkward', 'before', 'best', 'best actor',
                        'best actress', 'best director', 'boo', 'but', 'can', 'com', 'congrats', 'did', 'director',
                        'drama', 'fair', 'first', 'globe', 'globes', 'globes@', 'golden', 'golden globe',
                        'golden globes', 'goldenglobes', 'gq', 'hip hop', 'hollywood', 'hooray', 'http', 'i', 'it',
                        'looking', 'love', 'mejor', 'most', 'motionpicture', 'movie award', 'music award', 'news',
                        'nice', 'nshowbiz', 'piece', 'pop', 'rap', 'refinery29', 'rt', 'she', 'so', 'take', 'that',
                        'the', 'the golden globe', 'the golden globes', 'this year', 'tmz', 'usweekly', 'vanity',
                        'vanityfair', 'watching', 'we', 'what', 'while', 'yay', 'yeah']
combined_stopwords = stopwords + additional_stopwords
MAX_LENGTH = 10000  # constant used to take random sampling of tweets to shorten processing time


def get_all(year):
    winner_dict = get_winner(year)
    awards = OFFICIAL_AWARDS_1315
    nominee_dict = get_nominees(year)
    presenter_dict = get_presenters(year)

    for award in awards:
        print(award + ': ')
        print("winner: " + winner_dict[award])
        for nom in nominee_dict[award]:
            print("nominee: " + nom)
        print("presenters: " + presenter_dict[award] + "\n")


def get_names(text):
    person_list = []
    names = []
    for tweet in text:
        person_list += re.findall('([A-Z][a-z]+(?:\\s[A-Z][a-z]+)*)', " ".join(tweet))
    for word in person_list:
        if word not in combined_stopwords:
            names.append(word)

    return names


def get_hosts(year):
    '''Hosts is a list of one or more strings. Do NOT change the name
    of this function or what it returns.'''
    tweets = get_tweets(year)
    keyword = 'host'
    filterword = 'should'
    filtered_tweets = filter_tweets(tweets, [keyword], [filterword])
    print("CALLED GET TWEETS IN GET HOSTS")
    host_tweets = filtered_tweets
    host_names = {}

    nlp = spacy.load('en_core_web_sm')
    for tweet in host_tweets:
        doc = nlp(tweet)
        ents_list = doc.ents
        for ent in ents_list:
            if ent.label_ == 'PERSON' and ent.text not in combined_stopwords and ('#' and '@') not in ent.text:
                name = ent.text.lower()
                if name not in host_names:
                    host_names[name] = 0
                else:
                    host_names[name] += 1

    print("NAMES LOADED")

    hosts = [max(host_names, key=host_names.get)]
    if int(year) < 2018:
        compare_name = hosts[0]
        del host_names[compare_name]
        next_name = max(host_names, key=host_names.get)
        while compare_name in next_name or next_name in compare_name:
            compare_name = next_name
            next_name = max(host_names, key=host_names.get)
        hosts.append(next_name)

    return hosts


def get_awards(year):
    '''Awards is a list of strings. Do NOT change the name
    of this function or what it returns.'''
    # Your code here
    tweets = get_tweets(year)
    print("Year:", year)
    awards = []
    filtered = []
    ct = 0 # test count
    for tweet in tweets:
        if 'best' in tweet or 'Best' in tweet:
            ct += 1
            filtered.append(tweet.lower())

    # print("LEN OF FILTERED:", len(filtered)) # test count

    rbd = re.compile(r"(best\s[a-zA-z\s-]*drama)")
    rbm = re.compile(r"(best\s[a-zA-z\s-]*musical)")
    rbc = re.compile(r"(best\s[a-zA-z\s-]*comedy)")
    rbmp = re.compile(r"(best\s[a-zA-Z\s-]*motion picture)")
    rbt = re.compile(r"(best\s[a-zA-Z\s-]*television)")
    rbf = re.compile(r"(best\s[a-zA-Z\s-]*film)")


    for tweet in filtered:
        drama = re.search(rbd, tweet)
        musical = re.search(rbm, tweet)
        comedy = re.search(rbc, tweet)
        mopic = re.search(rbmp, tweet)
        tv = re.search(rbt, tweet)
        film = re.search(rbf, tweet)

        if drama:
            for s in drama.groups():
                award = str(s.lower())
                awards.append(award)
        elif musical and not comedy:
            for s in musical.groups():
                award = str(s.lower())
                awards.append(award)
        elif comedy:
            for s in comedy.groups():
                award = str(s.lower())
                awards.append(award)
        elif mopic:
            for s in mopic.groups():
                award = str(s.lower())
                awards.append(award)
        elif tv:
            for s in tv.groups():
                award = str(s.lower())
                awards.append(award)
        elif film:
            for s in film.groups():
                award = str(s.lower())
                awards.append(award)

    #print("COUNT OF TWEETS WITH 'BEST':", ct)
    #print(awards)
    freq = {}
    for items in awards:
        if len(items.split()) > 4 and 'tv' not in items and 'the' not in items:
            freq[items] = awards.count(items)

    for j in freq:
        for k in freq:
            if j == k:
                continue
            if j in k:
                freq[k] += freq[j]
                freq[j] = 0
                break

    sorted_by_freq = {k: v for k, v in sorted(freq.items(), key=lambda item: item[1], reverse=True)}
    best_awards = []
    i = 0
    for award in sorted_by_freq:
        if sorted_by_freq[award] > 10:
            print(sorted_by_freq[award])
            best_awards.append(award)
        i+=1
        if i > 25:
            break
    print(best_awards)
    print(len(best_awards))
    return best_awards


def get_relevant_tweets(tweets):
    # filter tweets based on loose constraints
    loose_keywords = ['best', 'cecil', 'demille', 'nominate', 'nominee']
    relevant_tweets = filter_tweets(tweets, [], loose_keywords, [])
    return relevant_tweets

def tag_tweets(year, tweets):
    # tag tweets with award category - creates dict of list of tweets, with award titles as keys
    if int(year) < 2016:
        awards_list = OFFICIAL_AWARDS_1315
        filter_dict = filter_dict_1819
    else:
        awards_list = OFFICIAL_AWARDS_1819
        filter_dict = filter_dict_1819

    # initialize dict with ALL award categories for autograder compatibility
    tagged_tweets = {key: [] for key in awards_list}
    print("TAGGED TWEETS INITIALIZED WITH LENGTH", len(tagged_tweets))
    for award in tagged_tweets:
        tagged_tweets[award] = filter_tweets(tweets, filter_dict[award][0], filter_dict[award][1], filter_dict[award][2])

    print("TAGGED TWEETS KEYS:", len(tagged_tweets), tagged_tweets.keys())
    return tagged_tweets


def get_nominee_counts(year, relevant_tweets):
    print("IN GET_NOMINEE_COUNTS, TWEETS DICT HAS LENGTH", len(relevant_tweets))
    # 2. identify named entities in each tag tweet - looks through dict of list of tweets and identifies
    #    the named entities in each tweet
    nlp = spacy.load('en_core_web_sm')
    named_entities = {key: [] for key in relevant_tweets}
    for award in relevant_tweets:
        for tweet in relevant_tweets[award]:
            doc = nlp(tweet)
            # if award is given to a person, filter out the named entities not are not people
            # print('AWARD NAME', award)
            # if 'actor' or 'actress' in award:
            #     ents_list = [ent for ent in doc.ents if ent.label_ == 'PERSON']
            #     #print("PERSON!", ents_list)
            # else:
            #     ents_list = [ent for ent in doc.ents if ent.label_ != 'PERSON']
            #     #print("NOT PERSON!", ents_list)
            ents_list = doc.ents
            for ent in ents_list:
                if ent.text not in combined_stopwords and '#' not in ent.text:
                    named_entities[award].append(ent.text.lower())  # make lowercase
    # print(len(named_entities), named_entities)

    # 3. count up each unique named entity in each category
    nominee_counts = {}
    for award, named_entities_list in named_entities.items():
        z = zip(Counter(named_entities_list).keys(), Counter(named_entities_list).values())
        sorted_named_entities = dict(sorted(z, key=lambda x: x[1], reverse=True))
        nominee_counts[award] = sorted_named_entities
    # return nominee_counts   ### REMINDER: COMMENTED OUT FOR TESTING

    # 4. get the named entities associated with the top 5 counts (5 nominees are selected per category in ggs)
    # highest count is the winner, next 4 remain the nominees

    # nominee_counts = get_nominee_counts(year)
    nominees = {key: [] for key in nominee_counts}
    for award in nominee_counts:
        nominees[award] = sorted(nominee_counts[award], key=nominee_counts[award].get, reverse=True)[:5]

    return nominees


def get_nominees(year):
    '''Nominees is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change
    the name of this function or what it returns.'''
    relevant_tweets = tag_tweets(year)
    nominees = get_nominee_counts(year, relevant_tweets)
    print("NOMINEES:", nominees)
    return nominees


def get_winner(year):
    '''Winners is a dictionary with the hard coded award
    names as keys, and each entry containing a single string.
    Do NOT change the name of this function or what it returns.'''
    print("GETTING WINNERS...")
    relevant_tweets = tag_tweets(year)
    nominees = get_nominee_counts(year, relevant_tweets)
    winners = {}
    for award in nominees:
        if nominees[award]:
            winners[award] = nominees[award][0]  # first element is the nominee with highest count
        else:
            winners[award] = ''
    print("WINNERS:", winners)
    return winners


def get_presenters(year):
    '''Presenters is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change the
    name of this function or what it returns.'''
    presenter_tweets = tag_tweets(year, presenters=True)
    nominees = get_nominee_counts(year, presenter_tweets)
    presenters = {}
    for award in nominees:
        if nominees[award]:
            presenters[award] = nominees[award][0]  # first element is the nominee with highest count
        else:
            presenters[award] = ''
    print("WINNERS:", presenters)
    return presenters


def pre_ceremony():
    '''This function loads/fetches/processes any data your program
    will use, and stores that data in your DB or in a json, csv, or
    plain text file. It is the first thing the TA will run when grading.
    Do NOT change the name of this function or what it returns.'''
    # global GLOBAL_TWEETS
    # GLOBAL_TWEETS = get_tweets(year, tokenize=False)
    print("Pre-ceremony processing complete.")
    return


def main():
    '''This function calls your program. Typing "python gg_api.py"
    will run this function. Or, in the interpreter, import gg_api
    and then run gg_api.main(). This is the second thing the TA will
    run when grading. Do NOT change the name of this function or
    what it returns.'''
    # Your code here
    while True:
        year = input("Award year: ")
        print(
            "Options:\n1. Get Hosts\n2. Get Awards\n3. Get Nominees\n4. Get Winners\n5. Get Presenters\n6. Read All\nx. Exit Program")
        entry = input("Enter option: ")
        if entry == '1':
            hosts = get_hosts(year)
            print(hosts)
        elif entry == '2':
            awards = get_awards(year)
            print(awards)
            # other methods not currently supported, though autograder will run them anyway
        elif entry == '3':
            nominees = get_nominees(year)
            print(nominees)
        elif entry == '4':
            winners = get_winner(year)
            print(winners)
        elif entry == '6':
            get_all(year)
        elif entry == "x":
            sys.exit()
        else:
            print("Invalid input")
    return


if __name__ == '__main__':
    # year = '2013' # change this to edit year
    pre_ceremony()
    main()
