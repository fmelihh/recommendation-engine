import dash
import random
import requests
import pandas as pd
import plotly.express as px
from dash import dcc, html, Input, Output, State

app = dash.Dash(__name__)
app.title = "Recommendation Engine"

app.layout = html.Div([
    html.H1("Restaurants", style={"textAlign": "center"}),
    html.Div([
        dcc.Input(
            id="search-box",
            type="text",
            placeholder="Enter search term",
            style={"width": "50%", "padding": "10px"}
        ),
        html.Button("Search", id="search-button", n_clicks=0, style={"marginLeft": "10px"}),
    ], style={"textAlign": "center", "margin": "20px"}),
    dcc.Graph(id="map-display"),
])

@app.callback(
    Output("map-display", "figure"),
    [Input("search-button", "n_clicks")],
    [State("search-box", "value")]
)
def update_map(n_clicks, search_term):
    if not search_term:
        # Show empty map if no search term is provided
        return px.scatter_mapbox(
            lat=[],
            lon=[],
            zoom=5,
            center={"lat": 39.0, "lon": 35.0},
            mapbox_style="open-street-map",
            title="No Data"
        )

    api_url = f"http://localhost:8001/search/search_text?search_text={search_term}&page_size=1000000"
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return px.scatter_mapbox(
            lat=[], lon=[], zoom=1,
            mapbox_style="open-street-map",
            title="Error fetching data"
        )

    # Convert data to DataFrame
    df = pd.DataFrame(data["results"])
    df["lat"] = df["lat"].apply(lambda x: float(x) + random.uniform(-0.05, 0.05))
    df["lon"] = df["lon"].apply(lambda x: float(x) + random.uniform(-0.05, 0.05))

    if df.empty or "lat" not in df.columns or "lon" not in df.columns:
        return px.scatter_mapbox(
            lat=[],
            lon=[],
            zoom=5,
            center={"lat": 39.0, "lon": 35.0},
            mapbox_style="open-street-map",
            title="No Results Found"
        )

    # Generate map figure
    fig = px.scatter_mapbox(
        df,
        lat="lat",
        lon="lon",
        zoom=7,
        hover_data={
            "restaurant_name": True,
            "restaurant_rate": True,
            "comment_avg_rating": True,
            "score": True
        },
        mapbox_style="open-street-map"
    )
    fig.update_layout(title=f"Restaurants {search_term}")

    return fig

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
