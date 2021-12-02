import json
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

sqliteConnection = sqlite3.connect('db/twitter_data.db')
cursor = sqliteConnection.cursor()

followers = api.get_followers(screen_name = name)
followers_list = []
for follower in followers:
    if True:
        string = json.dumps(follower._json)
        json_data = json.loads(string)
        each_follower_list = []
        each_follower_list.append(json_data["id"])
        each_follower_list.append(json_data["name"])
        each_follower_list.append(json_data["location"])
        followers_list.append(each_follower_list)

        cursor.execute( """CREATE TABLE IF NOT EXISTS followers
                                    (id INT(1000) NOT NULL, 
                                    name text NOT NULL,
                                    location text);""")
        df = pd.DataFrame(followers_list, columns=["id", "name", "location"])
        df.to_sql("followers", sqliteConnection, if_exists='append', index=False)
        sqliteConnection.commit()

print("Mission complete !!!")
