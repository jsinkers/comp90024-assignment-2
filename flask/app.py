from flask import Flask, jsonify, request, make_response, url_for, send_from_directory
from flask_restful import Resource, Api, abort

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


class Analytics(Resource):
    def get(self):
        return analytics

class Scenario(Resource):
    def get(self, scenario_id):
        abort_if_scenario_doesnt_exist(scenario_id)
        return analytics[scenario_id]


api.add_resource(Analytics, '/api/analytics/')
api.add_resource(Scenario, '/api/analytics/<scenario_id>')
