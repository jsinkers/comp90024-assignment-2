# Turns on debugging features in Flask
DEBUG = True
# IP address of couchDB
COUCHDB_IP = '172.26.131.244'
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
VIEW_FOR_ELECTION = "election_tweets"
VIEW_FOR_SOCIAL = "social_tweets"
