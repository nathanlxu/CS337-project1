'''Version 0.35'''
import sys
import nltk
import spacy
import itertools
from gg_utils import *
from collections import Counter
from random import sample
from collections import OrderedDict
import re
from difflib import SequenceMatcher

OFFICIAL_AWARDS_1315 = ['cecil b. demille award', 'best motion picture - drama', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best motion picture - comedy or musical', 'best performance by an actress in a motion picture - comedy or musical', 'best performance by an actor in a motion picture - comedy or musical', 'best animated feature film', 'best foreign language film', 'best performance by an actress in a supporting role in a motion picture', 'best performance by an actor in a supporting role in a motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best television series - comedy or musical', 'best performance by an actress in a television series - comedy or musical', 'best performance by an actor in a television series - comedy or musical', 'best mini-series or motion picture made for television', 'best performance by an actress in a mini-series or motion picture made for television', 'best performance by an actor in a mini-series or motion picture made for television', 'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television', 'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television']
OFFICIAL_AWARDS_1819 = ['best motion picture - drama', 'best motion picture - musical or comedy', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best performance by an actress in a motion picture - musical or comedy', 'best performance by an actor in a motion picture - musical or comedy', 'best performance by an actress in a supporting role in any motion picture', 'best performance by an actor in a supporting role in any motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best motion picture - animated', 'best motion picture - foreign language', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best television series - musical or comedy', 'best television limited series or motion picture made for television', 'best performance by an actress in a limited series or a motion picture made for television', 'best performance by an actor in a limited series or a motion picture made for television', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best performance by an actress in a television series - musical or comedy', 'best performance by an actor in a television series - musical or comedy', 'best performance by an actress in a supporting role in a series, limited series or motion picture made for television', 'best performance by an actor in a supporting role in a series, limited series or motion picture made for television', 'cecil b. demille award']

nltk.download('stopwords')
stopwords = nltk.corpus.stopwords.words('english')
stopwordsList = stopwords + ['The Golden Globes', 'the Golden Globes', 'the Golden Globe', 'GoldenGlobes', 'Golden', 'Globes', 'Golden Globes', 'RT', 'VanityFair', 'golden', 'globes' '@', 'I', 'we', 'http', '://', '/', 'com', 'Best', 'best', 'Looking','Nice', 'Most', 'Pop', 'Hip Hop', 'Rap', 'We', 'Love', 'Awkward','Piece', 'While', 'Boo', 'Yay', 'Congrats', 'And', 'The', 'Gq', 'Refinery29', 'USWeekly', 'TMZ', 'Hollywood', 'Watching', 'Hooray', 'That', 'Yeah', 'Can', 'So', 'And', 'But', 'What', 'NShowBiz', 'She', 'Mejor', 'Did', 'Vanity', 'Fair', 'Drama', 'MotionPicture', 'News', 'Take', 'Before', 'Director', 'Award', 'Movie Award', 'Music Award', 'Best Director', 'Best Actor', 'Best Actress', 'Am', 'Golden Globe', 'Globe', 'Awards', 'It', 'first','this year']
MAX_LENGTH = 20000 # constant used to take random sampling of tweets to shorten processing time
GLOBAL_YEAR = ['2013']
GLOBAL_TWEETS = get_tweets(GLOBAL_YEAR[0], tokenize=False)


def get_names(text):
    person_list = []
    names = []
    for tweet in text:
        person_list += re.findall('([A-Z][a-z]+(?:\\s[A-Z][a-z]+)*)'," ".join(tweet))
    for word in person_list:
        if word not in stopwordsList:
            names.append(word)

    return names

def get_hosts(year):
    '''Hosts is a list of one or more strings. Do NOT change the name
    of this function or what it returns.'''
    GLOBAL_YEAR[0] = year
    tweets = get_tweets(GLOBAL_YEAR[0])
    cnt = Counter()
    host_tweets = []
    hosts = []

    for tweet in tweets:
        if 'hosting' in tweet or 'hosted' in tweet:
            host_tweets.append(tweet)

    names = get_names(host_tweets)
    
    for name in names:
        cnt[name] += 1
    count = 1
    for word, value in cnt.most_common(2):
        #note - this approach assumes two hosts, which is true for about half of the Golden Globes to date
        #because of the huge variety of name conventions, stage names, and cultures, proper name validation beyond just finding apital words is tricky
        hosts.append(word)
    #print('Hosts:')
    return hosts

def process(award, year):
    #will need additional adjustments for post-2016 awards, like best actor in a supporting role in a motion role in A motion picture -> in ANY motion picture 
    if int(year) < 2016:
        com = ' - comedy or musical '
    else:
        com = ' - musical or comedy '

    if ' film ' in award:
        award = award.replace('film', 'motion picture')
    if 'movie' in award:
        award = award.replace('movie', 'motion picture')
    if 'picture' in award and 'motion' not in award:
        award = award.replace('picture', 'motion picture')
    if ' tv' in award:
        award = award.replace(' tv', ' television')
    if 'actor' in award:
        replacement = 'performance by an actor'
        if 'supporting ' in award:
            award = award.replace('supporting ', '')
            replacement += ' in a supporting role'
        if ' television series ' in award:
            award = award.replace('television series ', '')
            replacement += ' in a television series'
        award = award.replace('actor', replacement)
    if 'actress' in award:
        replacement = 'performance by an actress'
        if 'supporting ' in award:
            award = award.replace('supporting ', '')
            replacement += ' in a supporting role'
        if ' television series ' in award:
            award = award.replace('television series ', '')
            replacement += ' in a television series'
        award = award.replace('actress', replacement)
    if 'television' in award and 'series' not in award:
        award = award.replace('television', 'television series')
    if ' in a - ' in award:
        award = award.replace(' in a - ', ' - ')
    award = award.strip()

    if award in ['best - drama', 'best - comedy or musical', 'best - motion picture', 'best film', 'best - motion picture', 'best television']:
        award = None
    return award

def get_awards(year):
    '''Awards is a list of strings. Do NOT change the name
    of this function or what it returns.'''
    # Your code here
    tweets = get_tweets(year)
    print("Year:", year)
    cutoff_year = 2016 # year when category names underwent minor changes
    awards = []
    if int(year) < cutoff_year:
        com = ' - comedy or musical '
    else:
        com = ' - musical or comedy '
    filtered = []
    ct = 0 # test count
    for tweet in tweets:
        if 'Best' in tweet or 'best' in tweet:
            ct += 1
            current_word_list = re.findall(r"['a-zA-Z]+\b", ' '.join(tweet))
            filtered.append(' '.join(current_word_list))

    # print("LEN OF FILTERED:", len(filtered)) # test count

    rbd = re.compile(r"(Best\s[a-zA-z\s-]*Drama)")
    rbm = re.compile(r"(Best\s[a-zA-z\s-]*Musical)")
    rbc = re.compile(r"(Best\s[a-zA-z\s-]*Comedy)")
    rbmp = re.compile(r"(Best\s[a-zA-Z\s-]*Motion Picture)")
    rbt = re.compile(r"(Best\s[a-zA-Z\s-]*Television)")
    rbf = re.compile(r"(Best\s[a-zA-Z\s-]*Film)")

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
                award = award.replace(' drama', ' - drama')
                awards.append(process(award.strip(), year))
        elif musical and not comedy:
            for s in musical.groups():
                award = str(s.lower())
                if ' musical' in award and 'comedy' not in award:
                    award = award.replace(' musical', com)
                if int(year) < cutoff_year:
                    if ' - musical or comedy ' in award:
                        award = award.replace(' - musical or comedy ', com)
                else:
                    if ' - comedy or musical ' in award:
                        award = award.replace(' - comedy or musical ', com)
                awards.append(process(award.strip(), year))
        elif comedy:
            for s in comedy.groups():
                award = str(s.lower())
                if ' comedy' in award and 'musical' not in award:
                    award = award.strip().replace(' comedy', com)
                if int(year) < cutoff_year:
                    if ' - musical or comedy ' in award:
                        award = award.replace(' - musical or comedy ', com)
                else:
                    if ' - comedy or musical ' in award:
                        award = award.replace(' - comedy or musical ', com)
                awards.append(process(award.strip(), year))
        elif mopic:
            for s in mopic.groups():
                award = str(s.lower())
                awards.append(process(award.strip(), year))
        elif tv:
            for s in tv.groups():
                award = str(s.lower())
                awards.append(process(award.strip(), year))
        elif film:
            for s in film.groups():
                award = str(s.lower())
                awards.append(process(award.strip(), year))

    awards = [award[0] for award in nltk.FreqDist(awards).most_common(len(OFFICIAL_AWARDS_1315)) if award[0] is not None]
    print("COUNT OF TWEETS WITH 'BEST':", ct)
    print(awards)
    return awards

def filter_tweets(tweets, keywords):
    return [tweet for tweet in tweets if any(keyword in tweet for keyword in keywords)]

def tag_tweets(year):
    if int(year) < 2016:
        awards_list = OFFICIAL_AWARDS_1315
    else:
        awards_list = OFFICIAL_AWARDS_1819

    nltk.download('stopwords', quiet=True)
    stopwords = nltk.corpus.stopwords.words('english')
    stopwords_list = stopwords + ['award', 'best', 'motion picture', 'motion', 'picture', 'mopic' 'film', 'performance',
                                  'by', 'an', 'in', 'a', '-', 'or', ',', 'made', 'mini-series', 'role', 'original']
    # 1. tag tweets with award category - creates dict of list of tweets, with award titles as keys
    # tweets = get_tweets(year, tokenize=False)
    tweets = GLOBAL_TWEETS # changed to accept a preprocessed collection of tweets
    award_keywords = get_award_keywords(awards_list, stopwords_list)

    print("GOT TWEETS! NOW FILTERING...")
    filter_keywords = ['Best', 'best', 'Cecil', 'cecil', 'nominated', 'nominee', 'nominees']
    filtered_tweets = filter_tweets(tweets, filter_keywords)
    if len(filtered_tweets) > MAX_LENGTH:
        sampled_tweets = sample(filtered_tweets, MAX_LENGTH)
    else:
        sampled_tweets = filtered_tweets
    print("FILTERED AND SAMPLED! TWEETS IS OF LENGTH", len(sampled_tweets))
    # initialize dict with ALL award categories for autograder compatibility
    relevant_tweets = {key: [] for key in awards_list}
    print("TWEETS DICT INITIALIZED WITH LENGTH", len(relevant_tweets))

    for tweet in sampled_tweets:
        for award in award_keywords:
            if all(kw in tweet for kw in award_keywords[award]):
                relevant_tweets[award].append(tweet)
    # print(len(relevant_tweets), relevant_tweets.keys())
    return relevant_tweets

def get_nominee_counts(year):
    relevant_tweets = tag_tweets(year)
    print("IN GET_NOMINEE_COUNTS, TWEETS DICT HAS LENGTH", len(relevant_tweets))
    # 2. identify named entities in each tag tweet - looks through dict of list of tweets and identifies
    #    the named entities in each tweet
    nlp = spacy.load('en_core_web_sm')
    named_entities = {key: [] for key in relevant_tweets}
    for award in relevant_tweets:
        for tweet in relevant_tweets[award]:
            doc = nlp(tweet)
            # if award is given to a person, filter out the named entities not are not people
            # if 'actor' or 'actress' in award:
            #     ents_list = [ent for ent in doc.ents if ent.label_ == 'PERSON']
            # else:
            #     ents_list = doc.ents # [ent for ent in doc.ents if ent.label_ != 'PERSON']
            ents_list = doc.ents
            for ent in ents_list:
                if ent.text not in stopwordsList and '#' not in ent.text:
                    named_entities[award].append(ent.text.lower()) # make lowercase
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

TOP_NOMINEES = get_nominee_counts(GLOBAL_YEAR[0])

def get_nominees(year):
    '''Nominees is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change
    the name of this function or what it returns.'''
    nominees = TOP_NOMINEES
    print("NOMINEES:", nominees)
    return nominees

def get_winner(year):
    '''Winners is a dictionary with the hard coded award
    names as keys, and each entry containing a single string.
    Do NOT change the name of this function or what it returns.'''
    print("GETTING WINNERS...")

    # nominee_counts = get_nominee_counts(year)
    # nominee_counts = GLOBAL_NOMINEE_COUNTS
    nominees = TOP_NOMINEES
    # winners = {key: [] for key in nominee_counts}
    # for award in nominee_counts:
    #     if nominee_counts[award]:
    #         winners[award] = max(nominee_counts[award], key=nominee_counts[award].get)
    winners = {}
    for award in nominees:
        if nominees[award]:
            winners[award] = nominees[award][0] # first element is the nominee with highest count
        else:
            winners[award] = ''
    print("WINNERS:", winners)
    return winners

def get_presenters(year):
    '''Presenters is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change the
    name of this function or what it returns.'''
    # Your code here
    presenters = {}
    for element in OFFICIAL_AWARDS_1315:
        presenters[element] = ""
    return presenters

def pre_ceremony():
    '''This function loads/fetches/processes any data your program
    will use, and stores that data in your DB or in a json, csv, or
    plain text file. It is the first thing the TA will run when grading.
    Do NOT change the name of this function or what it returns.'''
    # if len(sys.argv) > 1:
    #     if '2013' in sys.argv:
    #         year = '2013'
    #     elif '2015' in sys.argv:
    #         year = '2015'
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
        print("Options:\n1. Get Hosts\n2. Get Awards\n3. Get Nominees\n4. Get Winners\n5. Get Presenters\nx. Exit Program")
        entry = input("Enter option: ")
        if entry == '1':
            hosts = get_hosts(year)
            print(hosts)
        elif entry == '2':
            awards = get_awards(year)
            print(awards)
            #other methods not currently supported, though autograder will run them anyway
        elif entry == '3':
            nominees = get_nominees(year)
            print(nominees)
        elif entry == '4':
            winners = get_winner(year)
            print(winners)
        elif entry == "x":
            sys.exit()
        else:
            print ("Invalid input")
    return

if __name__ == '__main__':
    pre_ceremony()
    main()
