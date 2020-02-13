'''Version 0.35'''
import sys
import re
import nltk
import spacy
from collections import Counter
from gg_utils import *
from random import sample



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
                   'best mini-series or motion picture made for television':[['picture','television'],['motion','picture','television','limited','series'],['actor','actress']],
                   'best performance by an actress in a mini-series or motion picture made for television':[['actress'],['television','tv','show','series','mini-series','mini-series'],['drama','comedy','supporting']],
                   'best performance by an actor in a mini-series or motion picture made for television':[['actor'],['television','tv','show','series','mini-series','mini-series'],['drama','comedy','supporting']],
                   'best performance by an actress in a television series - drama':[['actress','drama'],['television','tv','series'],['motion','picture']],
                   'best performance by an actor in a television series - drama':[['actor','drama'],['television','tv','series'],['motion','picture']],
                   'best performance by an actress in a television series - comedy or musical':[['actress','comedy'],['television','tv','series'],['motion','picture']],
                   'best performance by an actor in a television series - comedy or musical':[['actor','drama'],['television','tv','series'],['motion','picture']],
                   'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television':[['actress','supporting'],['television','tv','show','limited','series','mini-series','mini-series'],[]],
                   'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television':[['actor','supporting'],['television','tv','show','limited','series','mini-series','mini-series'],[]],
                   'cecil b. demille award':[[],['cecil','demille'],[]]}

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
                   'best performance by an actress in a supporting role in a series, limited series or motion picture made for television':[['actress','supporting'],['television','tv','limited','series'],[]],
                   'best performance by an actor in a supporting role in a series, limited series or motion picture made for television':[['actor','supporting'],['television','tv','limited','series'],[]],
                   'cecil b. demille award':[[],['cecil','demille'],[]]}

nltk.download('stopwords')
stopwords = nltk.corpus.stopwords.words('english')
additional_stopwords = ['/', '://', 'am', 'and', 'award', 'awards', 'awkward', 'before', 'best', 'best actor',
                        'best actress', 'best director', 'boo', 'but', 'can', 'com', 'congrats', 'did', 'director',
                        'drama', 'fair', 'first', 'globe', 'globes', 'globes@', 'golden', 'golden globe', 'goldenglobe',
                        'golden globes', 'goldenglobes', 'gq', 'hip hop', 'hollywood', 'hooray', 'http', 'i', 'it',
                        'looking', 'love', 'mejor', 'most', 'motionpicture', 'movie award', 'music award', 'news',
                        'nice', 'nshowbiz', 'piece', 'pop', 'rap', 'refinery29', 'rt', 'she', 'so', 'take', 'that',
                        'the', 'the golden globe', 'the golden globes', 'this year', 'tmz', 'netflix', 'twitter', 'usweekly', 'vanity', 'gq',
                        'vanityfair', 'watching', 'we', 'what', 'while', 'yay', 'yeah']
combined_stopwords = stopwords + additional_stopwords
MAX_LENGTH = 200000  # constant used to take random sampling of tweets to shorten processing time


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
    keyword = ['hosted', 'hosting']
    filterword = 'should'
    # filtered_tweets = filter_tweets(tweets, [keyword], [keyword], [filterword])
    filtered_tweets = [tweet for tweet in tweets if 'hosted' in tweet.lower() or 'hosting' in tweet.lower() and not 'should' in tweet.lower()]
    print("CALLED GET TWEETS IN GET HOSTS")
    host_tweets = filtered_tweets
    host_names = Counter()

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
    compare_name = hosts[0]

    while ' ' not in compare_name:
      del host_names[compare_name]
      compare_name = host_names.most_common(1)[0][0]
      hosts = [compare_name]

    if int(year) < 2018:
        next_name = host_names.most_common(1)[0][0]
        while compare_name in next_name or next_name in compare_name or ' ' not in next_name:
            del host_names[next_name]
            next_name = host_names.most_common(1)[0][0]
        hosts.append(next_name)

    print("GET HOSTS RETURNED:")
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
        filter_dict = filter_dict_1315
    else:
        awards_list = OFFICIAL_AWARDS_1819
        filter_dict = filter_dict_1819

    # initialize dict with ALL award categories for autograder compatibility
    tagged_tweets = {key: [] for key in awards_list}
    # print("TAGGED TWEETS INITIALIZED WITH LENGTH", len(tagged_tweets))
    # filter tweets for each award category given strict keywords, loose keywords, and filter words
    for award in tagged_tweets:
        # print("TWEETS OF LEN", len(tweets))
        tagged_tweets[award] = filter_tweets(tweets, filter_dict[award][0], filter_dict[award][1], filter_dict[award][2])

    # print("TAGGED TWEETS KEYS:", len(tagged_tweets), tagged_tweets.keys())
    return tagged_tweets


def get_named_entities(tagged_tweets):
    # looks through list of tweets in tagged tweets dict and identifies named entities in each tweet
    nlp = spacy.load('en_core_web_sm')
    named_entities = {key: [] for key in tagged_tweets}
    for award in tagged_tweets:
        for tweet in tagged_tweets[award]:
            doc = nlp(tweet)
            # if award is given to a person, filter out the named entities not are not people
            # print('AWARD NAME', award)
            # if ('actor' or 'actress') in award:
            #     ents_list = [ent for ent in doc.ents if ent.label_ == 'PERSON']
            #     # print("PERSON!", ents_list)
            # else:
            #     ents_list = [ent for ent in doc.ents if ent.label_ != 'PERSON']
                # print("NOT PERSON!", ents_list)
            ents_list = doc.ents
            for ent in ents_list:
                e = ent.text.lower()
                if e not in combined_stopwords and '#' not in e:
                    if e not in award:
                        names = ['actor', 'actress', 'director']
                        if any(n in award for n in names):
                            if len(e.split(' ')) == 2:
                                named_entities[award].append(e)
                        else:
                            named_entities[award].append(e)

    return named_entities


def count_named_entities(named_entities):
    # count up each unique named entity per award category
    named_entity_counts = {}
    for award, named_entities_list in named_entities.items():
        z = zip(Counter(named_entities_list).keys(), Counter(named_entities_list).values())
        sorted_named_entities = dict(sorted(z, key=lambda x: x[1], reverse=True))
        named_entity_counts[award] = sorted_named_entities

    return named_entity_counts


def top_k_nominees(named_entity_counts, k):
    top_nominees = {key: [] for key in named_entity_counts}
    for award in named_entity_counts:
        top_nominees[award] = sorted(named_entity_counts[award], key=named_entity_counts[award].get, reverse=True)[:k]

    return top_nominees


def get_nominees_and_winners(year):
    # tweets = to_lower_case(get_tweets(year)) # lower case tweets mess up the NER
    tweets = get_tweets(year)
    if len(tweets) > MAX_LENGTH:
        tweets = get_sample(tweets, MAX_LENGTH)
    relevant_tweets = get_relevant_tweets(tweets)
    tagged_tweets = tag_tweets(year, relevant_tweets)
    named_entities = get_named_entities(tagged_tweets)
    named_entities_count = count_named_entities(named_entities)
    top_nominees = top_k_nominees(named_entities_count, 5)

    nominees = {}
    winners = {}
    for award in top_nominees:
        nominees[award] = top_nominees[award][0:] # changed
        winners[award] = top_nominees[award][0]
    nominees['cecil b. demille award'] = nominees['cecil b. demille award'][0]

    print("GOT NOMINEES AND WINNERS")
    return nominees, winners


# NOMINEES, WINNERS = get_nominees_and_winners(2013)


def get_nominees(year):
    '''Nominees is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change
    the name of this function or what it returns.'''
    return get_nominees_and_winners(year)[0]


def get_winner(year):
    '''Winners is a dictionary with the hard coded award
    names as keys, and each entry containing a single string.
    Do NOT change the name of this function or what it returns.'''
    return get_nominees_and_winners(year)[1]


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

def get_red_carpet(year):
    #Additional Goal - return the top-mentioned celebrities on the Red Carpet and the kinds of superlative categories they fall under, broken down by most common compliments
    tweets = get_tweets(year)
    keywords = ['dazzling', 'dreamy', 'stunning', 'adorable', 'alluring', 'angelic', 'bewitching', 'classy', 'divine', 'transcendant', 'exquisite', 'gorgeous', 'grand', 'handsome', 'suave', 'flamboyant', 'juicy', 'nostalgic', 'cute']
    filtered_tweets = filter_tweets(tweets, [], keywords, [])
    fashion_tweets = filtered_tweets
    fashion_names = Counter()
    name_tweets = {}
    superlatives = {}

    nlp = spacy.load('en_core_web_sm')
    for tweet in fashion_tweets:
        keycount = 0
        for word in tweet.split():
            if word in keywords:
                keycount += 1
        doc = nlp(tweet)
        ents_list = doc.ents
        for ent in ents_list:
            if ent.label_ == 'PERSON' and ent.text not in combined_stopwords and ('#' and '@') not in ent.text:
                name = ent.text.lower()
                if name not in combined_stopwords:
                    if name not in fashion_names:
                        fashion_names[name] = keycount
                        name_tweets[name] = [tweet]
                    else:
                        fashion_names[name] += keycount
                        name_tweets[name].append(tweet)

    fashionistas = fashion_names.most_common(5)
    for fashionista in fashionistas:
        fashionista = fashionista[0]
        compliments = Counter()
        for tweet in name_tweets[fashionista]:
            tweet = tweet.split()
            for word in tweet:
                if word in keywords:
                    if word not in compliments:
                        compliments[word] = 1
                    else:
                        compliments[word] += 1
        superlatives[fashionista] = compliments

    for fashionista in fashionistas:
        fashionista = fashionista[0]
        print(fashionista)
        print(superlatives[fashionista].most_common(10))

    return fashionistas


def pre_ceremony():
    '''This function loads/fetches/processes any data your program
    will use, and stores that data in your DB or in a json, csv, or
    plain text file. It is the first thing the TA will run when grading.
    Do NOT change the name of this function or what it returns.'''
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
            "Options:\n1. Get Hosts\n2. Get Awards\n3. Get Nominees\n4. Get Winners\n5. Get Presenters\n6. Read All\n7. Red Carpet Superlatives\nx. Exit Program")
        entry = input("Enter option: ")
        if entry == '1':
            hosts = get_hosts(year)
            print(hosts)
        elif entry == '2':
            awards = get_awards(year)
            print(awards)
        elif entry == '3':
            nominees = get_nominees(year)
            print(nominees)
        elif entry == '4':
            winners = get_winner(year)
            print(winners)
        elif entry == '6':
            get_all(year)
        elif entry == '7':
            get_red_carpet(year) # **Additional Goal - return the top-mentioned celebrities on the red carpet and the kinds of superlative categories they fall under, broken down by most common compliments**
        elif entry == "x":
            sys.exit()
        else:
            print("Invalid input")
    return


if __name__ == '__main__':
    # year = '2013' # change this to edit year
    pre_ceremony()
    main()
