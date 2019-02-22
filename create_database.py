import mysql.connector
import config_database
config = {
  'user': config_database.USER,
  'password': config_database.PASSWORD,
  'host': config_database.HOST,
  'raise_on_warnings': config_database.RAISE_ON_WARNINGS
}

# define database
DB_NAME = 'crypt_twitter'

# define tables
TABLES = {}
TABLES['tweet'] = (
    "CREATE TABLE `tweet` ("
    "  `tweet_id` char(20) NOT NULL,"
    "  `tweet` varchar(280) NOT NULL,"
    "  `user_id` char(20) NOT NULL,"
    "  `symbol` char(10) NOT NULL,"
    "  `create_at` DATETIME NOT NULL,"  
    "  PRIMARY KEY (`tweet_id`)"
    ") ENGINE=InnoDB")

TABLES['symbol'] = (
    "CREATE TABLE `symbol` ("
    "  `tweet_id` char(20) NOT NULL,"
    "  `symbol` char(10) NOT NULL,"
    "  `create_at` DATETIME NOT NULL"  
    ") ENGINE=InnoDB")

cnx = mysql.connector.connect(**config)
cursor = cnx.cursor()
# create database

try:
    cursor.execute(
        "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
except mysql.connector.Error as err:
    print("Failed creating database: {}".format(err))
    #exit(1)

try:
    cursor.execute("USE {}".format(DB_NAME))
except mysql.connector.Error as err:
    print("Database {} does not exists.".format(DB_NAME))
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        create_database(cursor)
        print("Database {} created successfully.".format(DB_NAME))
        cnx.database = DB_NAME
    else:
        print(err)
        exit(1)

# create tables
for table_name in TABLES:
    table_description = TABLES[table_name]
    try:
        print("Creating table {}: ".format(table_name), end='')
        cursor.execute(table_description)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)
    else:
        print("OK")

cursor.close()
cnx.close()