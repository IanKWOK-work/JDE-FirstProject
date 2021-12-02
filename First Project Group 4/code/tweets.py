import pandas as pd
import tweepy
import sqlite3
import requests

# Api Connection

consumer_key = 'SNDhT4ZYKnM398eNo98HczpIC'  # my twitter API key & serect
consumer_serect = 'uEozE1tc7Fvlz5JbMWC4Ap8CkVvi3G9Vw9syu0rwsNfaNE8YkD'
access_token = '1447428831950688261-5LPYCfyhKdNW46Lc0JRIbIeTTw9KmA'
access_token_secret = 'mWyzY7sId3zRmKdXMUTduLyRgbG6SH2AXzV2SzxZ9hOmc'

auth = tweepy.OAuthHandler(consumer_key, consumer_serect)  # authentication
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)
name = '@JoeBiden'
tweetCount = 100  # return the 100 status(can change)
results = api.user_timeline(id=name, count=tweetCount)

whole_list = []
for tweet in results:
    # print(tweet)
    if True:
        try:
            list_ = []
            # Database connection
            sqliteConnection = sqlite3.connect('db/twitter_data.db')
            cursor = sqliteConnection.cursor()

            # Create table
            sqlite_Create_Query = """CREATE TABLE IF NOT EXISTS JoeBiden_Tweets
                                 (id INT(1000) NOT NULL, created_at VARCHAR(45) NOT NULL,
                                 tweet_text TEXT NOT NULL);"""

            cursor.execute(sqlite_Create_Query)

            # Set variables store the values from the retrieved data
            list_.append(tweet.id)
            list_.append(tweet.created_at)
            list_.append(tweet.text)
            # query = "INSERT INTO JoeBiden_Tweets (id, created_at, tweet_text) VALUES (?,?,?)"
            # cursor.execute(query, (a, b, c))
            whole_list.append(list_)
            df = pd.DataFrame(whole_list, columns=["id", "created_at", "tweet_text"])
            df.to_sql("JoeBiden_Tweets", sqliteConnection, if_exists='append', index=False)
            sqliteConnection.commit()

        except sqlite3.IntegrityError:
            print("DATA ALREADY EXISTED!!!!")


print("Mission complete !!!")
