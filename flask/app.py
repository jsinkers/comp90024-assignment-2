from flask import Flask, jsonify, request, make_response, url_for, send_from_directory
from flask_restful import Resource, Api, abort
import couchdb as db
import logging
from couchback_temp import CouchInterface

# for data preprocessing
import pandas as pd
from shapely.geometry import Polygon
import geopandas as gpd
import json

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

def join_languages_and_polygons(languages, polygons):
    # create df for both query outputs, join them, and export geojson string

    # preprocess the first query output
    for output in languages:
        # get the initial key-value pair
        sa2 = list(output.keys())[0]
        value = list(output.values())[0]

        if 'Proportion' in value:
            prop = value["Proportion"]
        # re-construct the dict
        output["sa2"] = sa2
        output["prop"] = prop
        del output[sa2]

    # preprocess the second query output
    for output in polygons:
        # get the initial key-value pair
        sa2 = list(output.keys())[0]
        value = list(output.values())[0]
        # re-construct the dict
        try:
            output["sa2"] = str(sa2)
            output["name"] = value['SA2_NAME16']
            rounded_polygon = [list(map(lambda x:round(x, 5), coords)) for coords in value['geometry'][0]]
            output["geometry"] = Polygon(rounded_polygon)
            del output[sa2]
        except(TypeError):
            # some empty geometry? can't get rounded_polygon
            del output[sa2]

    # create dataframes
    languages_df = pd.DataFrame(languages)
    polygons_df = pd.DataFrame(polygons)
    merged_df = languages_df.merge(polygons_df, on="sa2")
    polygon_gdf = gpd.GeoDataFrame(merged_df, geometry=merged_df["geometry"])

    # convert to json string
    return json.loads(polygon_gdf.to_json())

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
    def get(self):
        return analytics

class Tweets(Resource):
    # Return geojson format:
    # { "type": "Feature", “created_at”: xyz,
    #   "properties": { "compound": -0.5362, "text": "#auspol tweets",},
    #   "geometry": { "type": "Point", "coordinates": [ 144.95379890000001, -37.7740309 ] } }

    # initialize a CouchInterface object to retrive data from couchdb
    ci = create_couch_interface()


class Language(Resource):
    # Return geojson format:
    # { "type": "Feature", "properties": { "SA2_MAIN16": "206011105", "SA2_NAME16": "Brunswick", "prop_spk_other_lang": 0.30813904905155842 },
    #   "geometry": { "type": "Polygon", "coordinates": [ [ [ 144.94974, -37.76277 ], [ 144.95003, -37.76105 ] ] ] } }
    def get(self):
        # initialize a CouchInterface object to retrive data from couchdb
        ci = create_couch_interface()

        # load language info and polygons of sa2's from database
        sa2_languages = ci.non_grouped_results(db_name="aurin_lsahbsc_sa2", design_doc="filter", view_name="default")
        sa2_polygons = ci.non_grouped_results(db_name="abs_austgeo_sa2", design_doc="filter", view_name="default")

        # join two outputs, and output a geojson string
        return join_languages_and_polygons(sa2_languages, sa2_polygons)

class Sentiment(Resource):
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
            results = ci.grouped_results(db_name, design_doc, view_name)

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
        # return results


api.add_resource(Analytics, '/api/analytics/')
api.add_resource(Scenario, '/api/analytics/')
api.add_resource(Tweets, '/api/analytics/diversity/tweets/')
api.add_resource(Language, '/api/analytics/diversity/language/')
api.add_resource(Sentiment, '/api/analytics/diversity/sentiment/<string:scenario_id>/')


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
