import datetime
import mysql.connector
import config_database
import collections
import json
config_db = {
  'user': config_database.USER,
  'password': config_database.PASSWORD,
  'host': config_database.HOST,
  'database': 'crypt_twitter',
  'raise_on_warnings': config_database.RAISE_ON_WARNINGS
}

cnx = mysql.connector.connect(**config_db)
cursor = cnx.cursor(buffered=True)

query = ("SELECT symbol,tweet_id FROM tweet "
         "WHERE create_at BETWEEN %s AND %s")

hire_start = datetime.datetime.now() - datetime.timedelta(days = 1)
hire_end = datetime.datetime.now()

cursor.execute(query, (hire_start, hire_end))
symbols = cursor.fetchall()
symbol_list = []
for symbol in symbols:
  symbol_list.append(symbol[0])

print(symbol_list)
symbol_list = collections.Counter(symbol_list)
symbol_list_formed = []
for symbol in symbol_list:
    symbol_list_formed.append({'symbol':symbol,'count':symbol_list[symbol],'tweet':symbols[[x[0] for x in symbols].index(symbol)][1]})

print(symbol_list_formed)
with open('../popular_crypt_frontend/cryana/src/assets/crypt_name_list.json', 'w') as f:
    json.dump(symbol_list_formed, f, indent=2, ensure_ascii=False)

cursor.close()
cnx.close()