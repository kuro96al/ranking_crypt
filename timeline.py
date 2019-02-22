import twitter
import json, config #標準のjsonモジュールとconfig.pyの読み込み
import re
import collections
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

# Retrieve friends IDs
twitter_api = twitter.Twitter(auth=oauth)
friends = twitter_api.friends.ids(screen_name=SCREEN_NAME, count=5000)
friends_ids = ','.join(map(str, friends['ids']))

stream = twitter.TwitterStream(auth=oauth, secure=True)
for tweet in stream.statuses.filter(follow=friends_ids):
    if 'user' in tweet and tweet['user']['id'] in friends['ids']:
        print(tweet['user']['screen_name'], tweet['text'])
        expr = "\$[a-zA-Z]{3,10}|#[a-zA-Z]{3,10}"
        target_str = tweet['text']
        target_list = re.findall(expr, target_str)
        print(target_list)
        for target in target_list:
            target = re.sub("[\$,#]","",target)
            crypt_name_list.append(target)
            with open("crypt_text.txt") as f:
                 l = f.readlines()

            l.insert(0, target+'\n')
        print(crypt_name_list)
        crypt_name_list_counted = collections.Counter(crypt_name_list)
        print(crypt_name_list_counted)
        crypt_name_list_formed = []
        for key in crypt_name_list_counted:
            crypt_name_list_formed.append({'仮想通貨':key,'出現回数':crypt_name_list_counted[key]})
        print(crypt_name_list_formed)
        with open('../popular_crypt_frontend/cryana/src/assets/crypt_name_list.json', 'w') as f:
            json.dump(crypt_name_list_formed, f, indent=2, ensure_ascii=False)
