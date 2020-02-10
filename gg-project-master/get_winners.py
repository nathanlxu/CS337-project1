from gt import get_tweets
from award_keywords import award_keywords

awards_dict = award_keywords()
winners_dict = {}

tweets = get_tweets(2013)
for tweet in tweets:
    if "best" in tweet:
        for key in awards_dict:
            if all(word in tweet for word in awards_dict[key]):
                winners_dict[key] = tweet
                continue


print(winners_dict)