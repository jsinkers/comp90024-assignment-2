import couchdb as DB

userName = 'admin'
passWord = 'password'
url = 'http://' + userName + ':' + passWord + '@172.26.131.244:5984/'
server = DB.Server(url)
db = server['twitter']

for id in db:
    db.delete(db[id])