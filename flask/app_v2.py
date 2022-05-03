from flask import Flask, jsonify, request, make_response, url_for, send_from_directory
from flask_restful import Resource, Api, abort
import couchdb as db
import logging
from couchback_temp import CouchInterface

app = Flask(__name__)
app.config.from_object('config')

api = Api(app)

analytics = {
    'diversity': {'description': 'Diversity and the federal election'},
    'socioeconomic': {'description': 'Socioeconomic index and the federal election'}
}

def create_couch_interface():
    # initialize a CouchInterface object to retrive data from couchdb
    ci = CouchInterface(address=app.config["COUCHDB_IP"], port=str(app.config["COUCHDB_PORT"]),
    username=app.config["COUCHDB_USER"], password=app.config["COUCHDB_PASSWORD"])
    return ci

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
    return app.config['TWITTER_DB'].info()

class Analytics(Resource):
    def get(self):
        return analytics

class Scenario(Resource):
    def get(self, scenario_id):
        abort_if_scenario_doesnt_exist(scenario_id)

        # initialize a CouchInterface object to retrive data from couchdb
        ci = create_couch_interface()

        if(scenario_id=="diversity"):
            # get queried results in a list of dict: e.g.
            # {'214021380': {'sum': -1.1561, 'count': 2, 'min': -0.6808, 'max': -0.4753, 'sumsqr': 0.68939873}}
            db_name = app.config["COUCHDB_TWITTER_DB"]
            design_doc = app.config["DESIGN_DOC"]
            view_name = app.config["VIEW_FOR_ELECTION"]
            results = ci.grouping_results(db_name, design_doc, view_name)

            # convert into a dict of lists (like a dataframe)
            sa2s = sums = counts = []
            for result in results:
                sa2 = list(result.keys())[0]
                sa2s.append(sa2)
                sums.append(result[sa2]['sum'])
                counts.append(result[sa2]['count'])

            results_zipped = {'sa2':sa2s, 'sum':sums, 'count':counts}
            analytics[scenario_id]['returned_data'] = results_zipped

        return analytics[scenario_id]

"/personal-info/<string:name>"

api.add_resource(Analytics, '/api/analytics/')
api.add_resource(Scenario, '/api/analytics/<string:scenario_id>/')


# connect to database
couchdb_url = f'http://{app.config["COUCHDB_USER"]}:{app.config["COUCHDB_PASSWORD"]}@{app.config["COUCHDB_IP"]}:{app.config["COUCHDB_PORT"]}/'
app.logger.info("Connecting to couchDB...")
couchdb_server = db.Server(couchdb_url)
app.config['COUCHDB'] = couchdb_server
app.config['TWITTER_DB'] = couchdb_server[app.config["COUCHDB_TWITTER_DB"]]
app.logger.debug(app.config['TWITTER_DB'])
app.logger.info("Connected to couchDB")

if __name__ == "__main__":
    app.run(debug=app.config["DEBUG"])
