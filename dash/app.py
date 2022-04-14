from dash import Dash, dcc, html, Input, Output
import geopandas as gpd
import pandas as pd
import plotly.express as px

token = open(".mapbox_token").read()

#house_prices = pd.read_json('apm_sa3_2016_timeseries-4714135567381242866.json')
house_prices = pd.read_csv('apm_sa3_2016_timeseries-7226241202265206458.csv')
geojson = gpd.read_file('../frontend/SA3_2021_AUST_SHP_GDA2020-greater-melb.geojson') # replace with your own data source
fig = px.choropleth_mapbox(
    house_prices, geojson=geojson, color="sold_both_auction_private_treaty_medianprice",
    locations=" sa32016code", featureidkey="properties.SA3_CODE21",
    center={"lon": 144.9631, "lat": -37.8136}, zoom=9,
    range_color=[500000, 3000000],
    opacity=0.5
)

fig.update_layout(
    margin={"r":0,"t":0,"l":0,"b":0},
    autosize=True,
    mapbox_accesstoken=token
)
fig.update_layout(showlegend=False)

app = Dash(__name__)

app.layout = html.Div([
    dcc.Graph(id="fig", figure=fig, style={'position': 'absolute', 'top': 0, 'bottom': 0, 'width': '100vw', 'height': '100vh'}),
])

# @app.callback(
#     Output("graph", "figure"),
#     #Input("candidate", "value"))
#     )
# def display_choropleth():
#     house_prices = pd.read_json('apm_sa3_2016_timeseries-4714135567381242866.json')
#     geojson = gpd.read_file('../frontend/SA3_2021_AUST_SHP_GDA2020-greater-melb.geojson') # replace with your own data source
#     fig = px.choropleth_mapbox(
#         house_prices, geojson=geojson, #color=candidate,
#         locations="sa32016code", featureidkey="properties.SA3_CODE21",
#         center={"lat": 144.9631, "lon": -37.8136}, zoom=9,
#         range_color=[0, 6500])
#     fig.update_layout(
#         margin={"r":0,"t":0,"l":0,"b":0},
#         mapbox_accesstoken=token
#     )
#
#     return fig

app.run_server(debug=True, use_reloader=False)
