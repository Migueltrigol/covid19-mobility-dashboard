import pandas as pd
import os
import geopandas as gpd
import plotly.express as px
import dash
import dash_core_components as dcc
from dash.dependencies import Input, Output
import dash_html_components as html
import config


# Load preprocessed data
gdf = gpd.read_file(os.path.join(config.folder_data_preprocessed,config.geojson_filename_preprocessed_monthly))
df = pd.read_csv(os.path.join(config.folder_data_preprocessed,config.csv_filename_preprocessed))
timeframes = df["month"].unique().tolist()


# Create app
app = dash.Dash(
    __name__,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1.0"}
    ],
)
app.title = "Test"
server = app.server


# App layout
app.layout = html.Div(
    id="root",
    children=[
        html.Div(
            id="header",
            children=[
                html.A(
                    html.Img(id="logo", src=app.get_asset_url("dash-logo.png")),
                    href="https://plotly.com/dash/",
                ),
                html.H4(children="Covid-19 Mobility Response by Number of Journeys"),
                html.P(
                    id="description",
                    children=["Percentage of population by region and number of daily trips.",
                    html.Br(),
                    "Use the slider and the dropdown to select the month and to filter the views by the number of daily trips.", 
                    html.Br(),
                    "Lasso selection is also available in the map to choose desired municipalities and update the chart on the right-hand side, displaying daily trends."
                    ]
                ),
            ],
        ),
        html.Div(
            id="app-container",
            children=[
                html.Div(
                    id="left-column",
                    style={"width": "65%", "display": "inline-block"},
                    children=[
                        html.Div(
                            id="slider-container",
                            children=[
                                html.P(
                                    id="slider-text",
                                    children="Drag the slider to change the Month",
                                ),
                                dcc.Slider(
                                    id="timeframe-slider",
                                    min=min(timeframes),
                                    max=max(timeframes),
                                    value=min(timeframes),
                                    step=1,
                                    included=False,
                                    marks={
                                        str(timeframe): {
                                            "label": str(timeframe),
                                            "style": {"color": "#7fafdf"},
                                        }
                                        for timeframe in timeframes
                                    },
                                ),
                            ],
                        ),
                        html.Div(
                            id="heatmap-container",
                            children=[
                                html.P(
                                    id="heatmap-title",
                                ),
                                dcc.Graph(
                                    id="municipality-choropleth",
                                    figure=dict(
                                        layout=dict(
                                            mapbox=dict(
                                                layers=[],
                                                center=dict(
                                                    lat=40.4168, lon=-3.7038  
                                                ),
                                                pitch=0,
                                                zoom=4,
                                            ),
                                            autosize=True,
                                        ),
                                    ),
                                ),
                            ],
                        ),
                    ],
                ),
                html.Div(
                    id="right-column",
                    style={"width": "35%", "display": "inline-block"},
                    children=[
                        html.Div(
                            id="dropdown-container",
                            children=[
                                html.P(id="chart-selector", children="Select number of daily trips:"),
                                dcc.Dropdown(
                                    options=[
                                        {
                                            "label": "Two or More Journeys",
                                            "value": "2+",
                                        },
                                        {
                                            "label": "Two Journeys",
                                            "value": "2",
                                        },
                                        {
                                            "label": "One Journey",
                                            "value": "1",
                                        },
                                        {
                                            "label": "No Journeys",
                                            "value": "0",
                                        },
                                    ],
                                    value="2+",
                                    id="chart-dropdown",
                                ),
                            ],
                        ),
                        html.Div(
                            id="chart-container",
                            children=[
                                html.P(
                                id="chart-title",
                                ),
                                dcc.Graph(
                                    id="selected-data",
                                    figure=dict(
                                        data=[dict(x=0, y=0)],
                                        layout=dict(
                                            paper_bgcolor="#F4F4F8",
                                            plot_bgcolor="#F4F4F8",
                                            autofill=True,
                                            margin=dict(t=75, r=50, b=100, l=50),

                                        ),
                                    ),
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        ),
    ],
)


@app.callback(
    Output("municipality-choropleth", "figure"),
    [
    Input("timeframe-slider", "value"),
    Input("chart-dropdown", "value"),
     ],
)

def display_map(timeframe, number_of_trips):
    """Updates the map content given the timeframe and number_of_trips user filter selections.
    """
    dff=gdf[(gdf["month"]==timeframe) & (gdf["numero_viajes"]==number_of_trips)]
    fig = px.choropleth_mapbox(dff, 
                               geojson=dff["geometry"].__geo_interface__,
                            locations=dff.index2, color="%",
                            mapbox_style="carto-positron",
                            zoom=5, center={"lat": 40.4168, "lon": -3.7038},
                            opacity=0.5,
                            hover_data={'ID': True, "%": True, "index2": False}
                            )
    fig.update_traces(marker_line_width=0)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig


@app.callback(
    Output("selected-data", "figure"),
    [
        Input("municipality-choropleth", "selectedData"),
        Input("chart-dropdown", "value"),
        Input("timeframe-slider", "value"),
    ],
)

def display_selected_data(selectedData, number_of_trips, timeframe):
    """Updates the bar chart given the user filter selections (timeframe and number_of_trips) and the municipalities selected in the map (if any).
    """
    indexes=[]
    dfs=df.copy()
    dfs=dfs[dfs["month"]==timeframe]

    if selectedData is None:
        dfs_filtered= dfs.groupby(["date","numero_viajes"])["personas"].sum().to_frame("personas").reset_index(inplace=False)
        dfs_filtered["%"] = dfs_filtered["personas"]*100 / dfs_filtered.groupby(["date"])["personas"].transform('sum')
        dfs_filtered = dfs_filtered[dfs_filtered["numero_viajes"]==number_of_trips]
        fig = px.bar(dfs_filtered, x="date", y="%")
    else:
        pts = selectedData
        pts2=pts["points"]
        for i in pts2:
            indexes.append(i["location"])    
        selected= gdf[gdf["index2"].isin(indexes)]["ID"].unique()
        dfs_filtered= dfs[dfs["distrito"].isin(selected)]
        dfs_filtered= dfs_filtered.groupby(["date","numero_viajes"])["personas"].sum().to_frame("personas").reset_index(inplace=False)
        dfs_filtered["%"] = dfs_filtered["personas"]*100 / dfs_filtered.groupby(["date"])["personas"].transform('sum')
        dfs_filtered = dfs_filtered[dfs_filtered["numero_viajes"]==number_of_trips]
        fig = px.bar(dfs_filtered, x="date", y="%")

    fig_layout = fig["layout"]
    fig_layout["yaxis"]["title"] = "Percentage of Population"
    fig_layout["xaxis"]["title"] = ""
    fig_layout["yaxis"]["fixedrange"] = True
    fig_layout["xaxis"]["fixedrange"] = False
    fig_layout["hovermode"] = "closest"
    fig_layout["legend"] = dict(orientation="v")
    fig_layout["autosize"] = True
    fig_layout["paper_bgcolor"] = "#1f2630"
    fig_layout["plot_bgcolor"] = "#1f2630"
    fig_layout["font"]["color"] = "#2cfec1"
    fig_layout["xaxis"]["tickfont"]["color"] = "#2cfec1"
    fig_layout["yaxis"]["tickfont"]["color"] = "#2cfec1"
    fig_layout["xaxis"]["gridcolor"] = "#5b5b5b"
    fig_layout["yaxis"]["gridcolor"] = "#5b5b5b"
    
    return fig

if __name__ == "__main__":
    app.run_server(debug=False)

