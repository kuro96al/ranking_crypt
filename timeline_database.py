import twitter
import json, config #標準のjsonモジュールとconfig.pyの読み込み
import re
import collections
import sys, json, time, calendar


#sql
from datetime import date, datetime, timedelta
import mysql.connector
import config_database
config_db = {
  'user': config_database.USER,
  'password': config_database.PASSWORD,
  'host': config_database.HOST,
  'database': 'crypt_twitter',
  'raise_on_warnings': config_database.RAISE_ON_WARNINGS
}

SCREEN_NAME = 'write here'
crypt_name_list = []
# OAuth
ACCESS_TOKEN_KEY =  config.ACCESS_TOKEN
ACCESS_TOKEN_SECRET = config.ACCESS_TOKEN_SECRET
CONSUMER_KEY = config.CONSUMER_KEY
CONSUMER_SECRET = config.CONSUMER_SECRET

oauth = twitter.OAuth(ACCESS_TOKEN_KEY,
                      ACCESS_TOKEN_SECRET,
                      CONSUMER_KEY,
                      CONSUMER_SECRET)

def insert_tweet(tweet_id,tweet_text,user_id,symbols,time):
    cnx = mysql.connector.connect(**config_db)
    cursor = cnx.cursor()

    add_tweet = ("INSERT INTO tweet "
               "(tweet_id, tweet, user_id, symbol, create_at) "
               "VALUES (%s, %s, %s, %s, %s)")
    cursor.execute(add_tweet, (tweet_id,tweet_text,user_id,re.sub("[\$,#]","",symbols[0]).upper(),time))
    for symbol in symbols:
      symbol = re.sub("[\$,#]","",symbol).upper()
      add_symbol = ("INSERT INTO symbol "
               "(tweet_id, symbol, create_at) "
               "VALUES (%s, %s, %s)")
      cursor.execute(add_symbol, (tweet_id,symbol,time))
    cnx.commit()

# Retrieve friends IDs
twitter_api = twitter.Twitter(auth=oauth)
friends = twitter_api.friends.ids(screen_name=SCREEN_NAME, count=5000)
friends_ids = ','.join(map(str, friends['ids']))

stream = twitter.TwitterStream(auth=oauth, secure=True)
for tweet in stream.statuses.filter(follow=friends_ids):
    if 'user' in tweet and tweet['user']['id'] in friends['ids']:
        print(tweet['user']['screen_name'], tweet['text'])
        expr = "\$[a-zA-Z]{3,10}"
        non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), '')
        target_str = tweet['text']
        target_str = target_str.translate(non_bmp_map)
        target_list = list(set(re.findall(expr, target_str)))
        if target_list:
            time_utc = time.strptime(tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y')
            unix_time = calendar.timegm(time_utc)
            time_local = time.localtime(unix_time)
            japan_time = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
            insert_tweet(tweet['id_str'],target_str,tweet['user']['id_str'],target_list,japan_time)

