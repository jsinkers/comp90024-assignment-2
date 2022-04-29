from flask import Flask, jsonify, request, make_response, url_for
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


@app.route("/")
def index():
    # TODO: serve frontend app
    return "<p>Hello, World!</p>"

class Analytics(Resource):
    def get(self):
        return analytics

class Scenario(Resource):
    def get(self, scenario_id):
        abort_if_scenario_doesnt_exist(scenario_id)
        return analytics[scenario_id]


api.add_resource(Analytics, '/api/analytics/')
api.add_resource(Scenario, '/api/analytics/<scenario_id>')
