# Turns on debugging features in Flask
DEBUG = True
# IP address of couchDB
# 172.26.131.244: database-1
# 172.26.134.62: database-2
# 172.26.128.40: database-3
# 172.26.134.153: vm-4
COUCHDB_IP = '172.26.128.40'
# port of couchDB
COUCHDB_PORT = 5984
# username of couchDB
COUCHDB_USER = 'admin'
# password for couchDB
COUCHDB_PASSWORD = 'password'
# database for tweets
COUCHDB_TWITTER_DB = "twitter_historic"
# design doc name
DESIGN_DOC = "tweets"
# view name
VIEW_FOR_ELECTION = "election_sentiment_stats"
VIEW_FOR_SOCIAL = "socioeconomic_sentiment_stats"
# caching
CACHE_TYPE = "SimpleCache"
# 5 minutes default cache time
CACHE_DEFAULT_TIMEOUT = 300