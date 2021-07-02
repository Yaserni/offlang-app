import tweepy
import pandas as pd
import numpy as np


# http://www.tweepy.org/
# Get your Twitter API credentials and enter them here
consumer_key = "aXSfOJXuIokIrh6dKzQ8nkK1h"
consumer_secret = "lxVCXkQEWwMMTuvBok0W046eOYwERNPaeo2hXt1KAL7NuAaRu2"
access_key = "1328785313767051265-ks7Lgpp5Xish8JJTD8db85U6eShZhO"
access_secret = "ggQVZjnGAPXtJzoL2o0iyVzPw8jDJEcYCbv4L4mrwDc6l"

# method to get a user's last tweets


def get_tweets(username):
    # http://tweepy.readthedocs.org/en/v3.1.0/getting_started.html#api
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)
    # set count to however many tweets you want
    number_of_tweets = 50

    # get tweets
    tweets_for_csv = []
    for tweet in tweepy.Cursor(api.user_timeline, screen_name = username).items(number_of_tweets):
        # create array of tweet information:  tweet id, date/time, text
        tweets_for_csv.append([tweet.text])
    outfile = "profile_tweets.xlsx"
    numpy_data = np.array(tweets_for_csv)
    df = pd.DataFrame(data=numpy_data, columns=["info"])
    df.to_excel(outfile,index=False)
    return outfile
