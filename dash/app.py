from dash import Dash, dcc, html
import geopandas as gpd
import pandas as pd
import plotly.express as px

token = open(".mapbox_token").read()

house_prices = pd.read_csv('apm_sa3_2016_timeseries-7226241202265206458.csv')
geojson = gpd.read_file('../frontend/SA3_2021_AUST_SHP_GDA2020-greater-melb.geojson')
fig = px.choropleth_mapbox(
    house_prices, geojson=geojson, color="sold_both_auction_private_treaty_medianprice",
    locations=" sa32016code", featureidkey="properties.SA3_CODE21",
    center={"lon": 144.9631, "lat": -37.8136}, zoom=9,
    range_color=[500000, 3000000],
    opacity=0.5,
)

fig.update_layout(
    showlegend=False,
    margin={"r":0,"t":0,"l":0,"b":0},
    autosize=True,
    mapbox_accesstoken=token
)

app = Dash(__name__)

app.layout = html.Div([
    dcc.Graph(id="fig", figure=fig, style={'position': 'absolute', 'top': 0, 'bottom': 0, 'width': '100%', 'height': '100%'}),
])

app.run_server(debug=True, use_reloader=False)
