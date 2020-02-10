import nltk
from nltk.tokenize import word_tokenize 


def sort_by_values_len(dict):
    dict_len= {key: len(value) for key, value in dict.items()}
    import operator
    sorted_key_list = sorted(dict_len.items(), key=operator.itemgetter(1), reverse=True)
    sorted_dict = [{item[0]: dict[item [0]]} for item in sorted_key_list]
    return sorted_dict

def award_keywords():
    OFFICIAL_AWARDS_1315 = ['cecil b. demille award', 'best motion picture - drama', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best motion picture - comedy or musical', 'best performance by an actress in a motion picture - comedy or musical', 'best performance by an actor in a motion picture - comedy or musical', 'best animated feature film', 'best foreign language film', 'best performance by an actress in a supporting role in a motion picture', 'best performance by an actor in a supporting role in a motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best television series - comedy or musical', 'best performance by an actress in a television series - comedy or musical', 'best performance by an actor in a television series - comedy or musical', 'best mini-series or motion picture made for television', 'best performance by an actress in a mini-series or motion picture made for television', 'best performance by an actor in a mini-series or motion picture made for television', 'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television', 'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television']

    nltk.download('stopwords')
    stopwords = nltk.corpus.stopwords.words('english')
    stopwordsList = stopwords + ['award', 'best', 'motion picture', 'motion', 'picture', 'mopic' 'film', 'performance', 'by', 'an', 'in', 'a', '-', 'or', ',', 'made', 'mini-series', 'role', 'original']

    award_mapping = {}

    for award in OFFICIAL_AWARDS_1315:
        key_words = []
        award_tokens = word_tokenize(award)
        for words in award_tokens:
            if words not in stopwordsList:
                key_words.append(words)
        award_mapping[award] = key_words

    sorted_items = sorted(award_mapping.items(), key = lambda item : len(item[1]), reverse=True)
    sorted_dict = dict(sorted_items)
    #sorted_awards = sort_by_values_len(award_mapping)

    #print(award_mapping)
    #return sorted_awards
    #print(sorted_dict)

award_keywords()

