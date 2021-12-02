import pandas as pd
import tweepy
import sqlite3
import requests
from pandas.io.json import json_normalize

# Api Connection
consumer_key = 'SNDhT4ZYKnM398eNo98HczpIC'  # my twitter API key & serect
consumer_serect = 'uEozE1tc7Fvlz5JbMWC4Ap8CkVvi3G9Vw9syu0rwsNfaNE8YkD'
access_token = '1447428831950688261-5LPYCfyhKdNW46Lc0JRIbIeTTw9KmA'
access_token_secret = 'mWyzY7sId3zRmKdXMUTduLyRgbG6SH2AXzV2SzxZ9hOmc'

auth = tweepy.OAuthHandler(consumer_key, consumer_serect)  # authentication
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)
name = '@JoeBiden'

search_words = ["0", "1"]    # db added table in browser


# filter the tweets from covid, vaccination
counter = 0
big_list = []
for keyword in search_words:
    for JoeBiden_Tweets in tweepy.Cursor(api.search_tweets, tweet_mode='extended', q=keyword, lang="en").items(200):
        sqliteConnection = sqlite3.connect('db/twitter_data.db')
        cursor = sqliteConnection.cursor()
        filted_list = []
        filted_list.append(JoeBiden_Tweets.id)
        filted_list.append(JoeBiden_Tweets.created_at)
        filted_list.append(JoeBiden_Tweets.full_text)
        big_list.append(filted_list)
        cursor.execute("""CREATE TABLE IF NOT EXISTS filtered_text
                                            (id INT(1000) NOT NULL,
                                            created_at int,
                                            full_text text(1000) );""")

        df = pd.DataFrame(big_list,columns=["id", "created_at", "full_text"])
        df.to_sql("filtered_text", sqliteConnection, if_exists='append', index=False)
        sqliteConnection.commit()

print("Mission complete !!!")