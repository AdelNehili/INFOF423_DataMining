import dash_mantine_components as dmc
from dash import Dash, html, Input, Output, State, callback, dcc, dash_table
import plotly.express as px
import dash_leaflet as dl
import json
from utils import get_data_files, load_df, df_to_dict, filter_df, get_vehicule_ids, COLS

data = None

app = Dash(
    __name__,
    external_stylesheets=[
        # include google fonts
        "https://fonts.googleapis.com/css2?family=Inter:wght@100;200;300;400;500;900&display=swap"
    ]
)

app.layout = dmc.MantineProvider(
    theme={
        "fontFamily": "'Inter', sans-serif",
        "primaryColor": "indigo",
        "components": {
            "Button": {"styles": {"root": {"fontWeight": 400}}},
            "Alert": {"styles": {"title": {"fontWeight": 500}}},
            "AvatarGroup": {"styles": {"truncated": {"fontWeight": 500}}},
        },
    },
    inherit=True,
    withGlobalStyles=True,
    withNormalizeCSS=True,
    children=[
        dmc.Container(
            className="app-container",
            fluid=True,
            p=0,
            children=[
                dmc.Header(
                    className="app-header",
                    p="xs",
                    height="auto",
                    children=[
                        dmc.Title("Cool Train", order=1, size=25, variant="gradient")
                    ]
                ),
                dmc.Container(
                    className="main",
                    fluid=True,
                    p=0,
                    children=[
                        dmc.Aside(
                            className="aside",
                            p="xs",
                            width={"base": 300},
                            withBorder=False,
                            children=[
                                dmc.Select(
                                    label="Select dataset",
                                    placeholder="Select one",
                                    id="dataset-select",
                                    data=get_data_files(),
                                ),
                                dmc.MultiSelect(
                                    label="Select features",
                                    placeholder="",
                                    searchable=True,
                                    clearable=True,
                                    id="features-select",
                                    data=COLS
                                ),
                                dmc.MultiSelect(
                                    label="Select trains",
                                    placeholder="",
                                    searchable=True,
                                    clearable=True,
                                    id="trains-select",
                                    data=[]
                                )
                            ]
                        ),
                        dmc.Container(
                            className="content",
                            fluid=True,
                            p="xs",
                            children=[
                                html.Div(dash_table.DataTable(
                                    id="full-data",
                                    sort_action="native",
                                    sort_mode="single",
                                    page_size=10,
                                    style_cell={'textAlign': 'left'},
                                    style_table={'height': 'auto', 'overflowY': 'auto', 'overflowX': 'auto'}, 
                                )),
                                dl.Map(dl.TileLayer(), center=[50.50,4.47], zoom=7, style={'height': '50vh'})
                                # dcc.Graph(figure={}, id='logs-count-per-veh')
                            ]
                        )
                    ]
                ),
                
            ]
        ),
        dcc.Store(id="dataset-filter", data=""),
        dcc.Store(id="vehicules-filter", data=json.dumps([])),
        dcc.Store(id="features-filter", data=json.dumps([]))
    ],
)

@callback(Output("dataset-filter", "data"), Input("dataset-select", "value"))
def select_data_file(value):
    return value

@callback(Output("trains-select", "data"), Input("dataset-select", "value"))
def select_data_file(value):
    return get_vehicule_ids(load_df(value))

@callback(Output("features-filter", "data"), Input("features-select", "value"))
def select_features(value):
    return value

@callback(Output("vehicules-filter", "data"), Input("trains-select", "value"))
def select_features(value):
    return value

@callback(
    Output("full-data", "data"),
    Input("dataset-filter", "data"),
    Input("features-filter", "data"),
    Input("vehicules-filter", "data"),
)
def select_features(dataset_filter, features_filter, vehicules_filter):
    return df_to_dict(filter_df(load_df(dataset_filter), {"vehicules": vehicules_filter, "features": features_filter}))


if __name__ == '__main__':
    app.run(debug=True)