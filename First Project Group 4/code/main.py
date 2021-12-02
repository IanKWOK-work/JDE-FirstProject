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
    try:
        list_ = []
        # Database connection
        sqliteConnection = sqlite3.connect('db/twitter_data.db')
        cursor = sqliteConnection.cursor()

        # Create table
        sqlite_Create_Query = """CREATE TABLE IF NOT EXISTS JoeBiden_Tweets
                            (id INT(1000) NOT NULL primary key, created_at VARCHAR(45) NOT NULL,
                             tweet_text TEXT NOT NULL);"""

        cursor.execute(sqlite_Create_Query)
        print("Succeeded to create table")

        # sql = "INSERT INTO JoeBiden_Tweets (id, created_at, tweet) VALUES(?,?,?);", tweet
        # sqlite_Insert_Query = """"INSERT INTO JoeBiden_Tweets (id, created_at, tweet_text)
        #                        VALUES(?,?,?);",tweet"""
        # cursor.execute(sqlite_Insert_Query)
        # cursor.execute("""'.INSERT INTO JBCovidTweets (id, created_at, tweet) VALUES(?,?,?);',(id, created_at, tweet_text)""")

        # Set variables store the values from the retrieved data
        a = tweet.id
        b = tweet.created_at
        c = tweet.text
        list_.append(a)
        list_.append(b)
        list_.append(c)
        # query = "INSERT INTO JoeBiden_Tweets (id, created_at, tweet_text) VALUES (?,?,?)"
        # cursor.execute(query, (a, b, c))

        # Insert data
        #cursor.execute("INSERT INTO JoeBiden_Tweets VALUES (?,?,?)", (a, b, c))
        #sqliteConnection.commit()
        #print("Succeeded to insert value to the table")
        # print(a, b, c)

        #sqlite_Select_Query = """SELECT * FROM JoeBiden_Tweets;"""
        #cursor.execute(sqlite_Select_Query)
        #print("Succeeded to select data from the table")

        cursor.execute('''CREATE TABLE profile (
        user_id	INTEGER NOT NULL,
        name text,
        screen_name	text NOT NULL,
        location	text NOT NULL,
        description	text NOT NULL,
        create_at	INTEGER,
        followers_count	INTEGER,
        friends_count	INTEGER
        );''')
        print("Succeeded to create table profile")

        cursor.execute('''CREATE TABLE friends (
                    friend_id	INTEGER NOT NULL,
                    friends_name	text NOT NULL,
                    friends_location	INTEGER
                    )''')
        print("Succeeded to create table friends")

        cursor.execute('''CREATE TABLE followers (
            followers_id	INTEGER NOT NULL,
            followers_name	text NOT NULL,
            followers_location	INTEGER
            );''')
        print("Succeeded to create table followers")


        # Insert data
        cursor.execute("INSERT INTO profile VALUES (?,?,?,?,?,?,?,?,?,?)",
                       (tweet.id, tweet.screen_name, tweet.location, tweet.description, tweet.create_at
                        , tweet.followers_count, tweet.friends_count, tweet.statuses_count
                        ))
        sqliteConnection.commit()
        print("Succeeded to insert value to the table profile")


        cursor.execute("INSERT INTO friends VALUES (?,?,?)",
                       (tweet.id, tweet.name, tweet.count))  # friend_id or id?
        sqliteConnection.commit()
        print("Succeeded to insert value to the table friends")

        cursor.execute("INSERT INTO followers VALUES (?,?,?)",
                       (tweet.id, tweet.name, tweet.location))  # followers_id or id?
        sqliteConnection.commit()
        print("Succeeded to insert value to the table followers")



    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)

    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed.")



#Filt function
sqliteConnection = sqlite3.connect('db/twitter_data.db')
cursor = sqliteConnection.cursor()

JoeBiden_Tweet = cursor.execute( """SELECT * FROM JoeBiden_Tweets;""")
covid = cursor.execute("""SELECT * FROM covid;""")
vaccination = cursor.execute("""SELECT * FROM vaccination;""")

# define what tweets we are interested in
search_words = covid, vaccination    # db added table in browser

# filter the tweets from covid, vaccination
counter = 0
for JoeBiden_Tweets in tweepy.Cursor(api.search_tweets, tweet_mode='extended', q=search_words, lang="en").items():
        print('Tweet Downloaded: ', counter)
        print(tweet.full_text)
        counter+=1
        if counter >= 100:
            break

#insert filted text into covid, vaccination databases

