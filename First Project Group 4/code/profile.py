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
user = api.get_user(screen_name=name)
profile_list = []


sqliteConnection = sqlite3.connect('db/twitter_data.db')
cursor = sqliteConnection.cursor()

detail_profile = []
detail_profile.append(user.id)
detail_profile.append(user.name)
detail_profile.append(user.screen_name)
detail_profile.append(user.description)
detail_profile.append(user.followers_count)
detail_profile.append(user.friends_count)
detail_profile.append(user.location)
detail_profile.append(user.created_at)
profile_list.append(detail_profile)

cursor.execute("""CREATE TABLE IF NOT EXISTS profile
                                    (id INT(1000) NOT NULL, 
                                    name text NOT NULL,
                                    screen_name text NOT NULL,
                                    description text(1000),
                                    followers_count int,
                                    friends_count int,
                                    location text,
                                    created_at int );""")
df = pd.DataFrame(profile_list, columns=["id", "name", "screen_name", "description", "followers_count",
                                          "friends_count","location", "created_at"])
df.to_sql("profile", sqliteConnection, if_exists='append', index=False)
sqliteConnection.commit()

print("Mission complete !!!")





