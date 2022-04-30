from flask import Flask, jsonify, request, make_response, url_for, send_from_directory
from flask_restful import Resource, Api, abort
import couchdb as db

app = Flask(__name__)
app.config.from_object('config')

api = Api(app)

analytics = {
    'diversity': {'description': 'Diversity and the federal election'},
    'socioeconomic': {'description': 'Socioeconomic index and the federal election'}
}

def abort_if_scenario_doesnt_exist(scenario):
    if scenario not in analytics:
        abort(404, message="Todo {} doesn't exist".format(scenario))


# Svelte app
@app.route("/")
def index():
    return send_from_directory('../frontend/public', 'index.html')

# serve static files for the Svelte app
@app.route("/<path:path>")
def home(path):
    return send_from_directory('../frontend/public', path)

# Testing route
@app.route("/twitter_database_info")
def database_status():
    return twitter_db.info()

class Analytics(Resource):
    def get(self):
        return analytics

class Scenario(Resource):
    def get(self, scenario_id):
        abort_if_scenario_doesnt_exist(scenario_id)
        return analytics[scenario_id]


api.add_resource(Analytics, '/api/analytics/')
api.add_resource(Scenario, '/api/analytics/<scenario_id>')

if __name__ == "__main__":
    # connect to database
    couchdb_url = f'http://{app.config(COUCHDB_USER)}:{app.config(COUCHDB_PASSWORD)}@{app.config(COUCHDB_IP)}:{COUCHDB_PORT}/'
    print("Connecting to server...")
    couchdb_server = DB.Server(couchdb_url)
    twitter_db = self.server[app.config(COUCHDB_TWITTER_DB)]
    app.run(debug=app.config(DEBUG))
