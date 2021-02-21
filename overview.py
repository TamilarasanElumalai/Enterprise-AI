import dash
import pickle
import copy
import pathlib
import math
import datetime as dt
import pandas as pd
from dash.dependencies import Input, Output, State, ClientsideFunction
import dash_core_components as dcc
import dash_html_components as html
import utils
import dash_table
import plotly.graph_objects as go
import plotly.express as px

# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../data").resolve()

# Load data
df = pd.read_csv(DATA_PATH.joinpath("Data Science Bootcamp Data_2.0.csv"))
df = df[:500]
df_cluster = pd.read_csv(DATA_PATH.joinpath("ClusterData.csv"))
dfc = pd.read_csv(DATA_PATH.joinpath("clustering.csv"))


###############     Histogram   ###############################
fig = go.Figure()
fig.add_trace(go.Histogram(
    x = df_cluster['No of Years'][df_cluster['Gender'] == 'Male'],
    name='Male',
    xbins=dict(
        start = 0,
        end = 60,
        size = 5
    ),
    marker_color='#EB89B5',
    opacity=0.75
))

fig.add_trace(go.Histogram(
    x=df_cluster['No of Years'][df_cluster['Gender'] == 'Female'],
    name='Female',
    xbins=dict(
        start=0,
        end=60,
        size=5
    ),
    marker_color='#330C73',
    opacity=0.75
))

fig.update_layout(
    title_text='Age Distribution', # title of plot
    xaxis_title_text='Age', # xaxis label
    yaxis_title_text='Count', # yaxis label
    bargap=0.2, # gap between bars of adjacent location coordinates
    bargroupgap=0.1 # gap between bars of the same location coordinates
)
##############################################

############# Pie Chart Employment ############

fig2 = px.pie(df_cluster, names='Employment Category')

fig2.update_layout(
    title_text="Employement Distributions"
)

###############################################

############# Pie Chart Location ###############

fig3 = px.pie(df_cluster, names='Location')

fig3.update_layout(
    title_text="Location Distributions"
)

###############################################

############# Pie Chart Bank ###############

fig4 = px.pie(df_cluster, names='Bank')

fig4.update_layout(
    title_text="Bank Distributions"
)

###############################################


def create_layout(app):
    # Page layouts
    return html.Div(    ## External spare
        [   
            html.Div(       ## main container
                [
                    html.Div(
                        [
                            html.H3(
                                "Customer Segmentation",
                                style={"margin-bottom": "0%"},
                            )
                        ],
                        className="row flex-display",
                        id="header",
                    ),
                    html.Div(
                        [
                            html.Div(
                                [
                                    # html.P(
                                    #     "Filter by construction date (or select range in histogram):",
                                    #     className="control_label",
                                    # )
                                    html.Div(
                                        [
                                            dcc.Tabs(id="manhattan-tabs", value='what-is', children=[
                                                dcc.Tab(
                                                    label='Description',
                                                    value='what-is',
                                                    children=html.Div(className='control-tab', children=[
                                                        html.H4(className='what-is', children='What type of information present inside the dataset?'),
                                                        html.P('Dataset have the Demographics as well as Behavioral information '
                                                        'about the customer. '
                                                        'Take a closer look at a small subset of the data.'),
                                                        html.P('The Behavioral information is extracted from '
                                                        'feedback to the bank given by customer.')
                                                    ])
                                                ),

                                            ]
                                            )

                                        ],
                                        id="manhattan-tabs-parent"
                                    )
                                ],
                                id="cross-filter-options",
                                className="pretty_container four columns",
                            ),

                            html.Div(
                                [
                                    html.Div(
                                        [
                                            html.Div(
                                                [
                                                    html.H4(
                                                        "Dataset"
                                                    ),
                                                    #dcc.Graph(id="main_graph",figure=fig)
                                                    dash_table.DataTable(
                                                        id='table',
                                                        columns=[{"name": i, "id": i} for i in df.columns[1:]],
                                                        data=df.to_dict('records'),
                                                        style_table={'height': '300px', 'overflowY': 'auto', 'width':'100%'},
                                                    )
                                                ],
                                                id="countGraphContainer",
                                                className="pretty_container",
                                                style={"width":"100%"}
                                            )

                                        ],
                                        id="info-container",
                                        className="row container-display",
                                    )
                                ],
                                id="right-column",
                                className="eight columns",
                            )
                        ],
                        className="row flex-display"
                    ),
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Div(
                                        [
                                            dcc.Graph(id="main_graph",figure=fig)
                                        ],
                                        id="main_graph",
                                        className="dash-graph"
                                    )

                                ],
                                className="pretty_container seven columns"
                            ),

                            html.Div(
                                [
                                    html.Div(
                                        [
                                            dcc.Graph(id="main_graph2",figure=fig2)
                                        ],
                                        id="main_graph2",
                                        className="dash-graph"
                                    )

                                ],
                                className="pretty_container seven columns"
                            )

                        ],
                        className="row flex-display"
                    ),
                    ##### Row 3 ####

                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Div(
                                        [
                                            dcc.Graph(id="main_graph3",figure=fig3)
                                        ],
                                        id="main_graph",
                                        className="dash-graph"
                                    )

                                ],
                                className="pretty_container seven columns"
                            ),

                            html.Div(
                                [
                                    html.Div(
                                        [
                                            dcc.Graph(id="main_graph4",figure=fig4)
                                        ],
                                        id="main_graph",
                                        className="dash-graph"
                                    )

                                ],
                                className="pretty_container seven columns"
                            )

                        ],
                        className="row flex-display"
                    ),

                    ################
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Div(
                                        [
                                            dcc.Tabs(id="manhattan-tabs", value='cluster-1', children=[
                                                dcc.Tab(
                                                    label='Cluster 1',
                                                    value='cluster-1',
                                                    children=html.Div(className='control-tab', children=[
                                                        html.H4(className='cluster-1', children='Observations :- '),
                                                        html.Li('Average Age :- 29 years '),
                                                        html.Li('Average Income :- 64,500 '),
                                                        html.Li('Average Loyalty :- 5 years '),
                                                        html.Li('Average Branch Frequency :- 3 times a month '),
                                                        html.Li('Average ATM Frequency : 7 times a month '),
                                                        html.Li('Average Internet Frequency : 1 times a month '),
                                                        html.Li('From cust_care_score, complaints_score, val_for_money_score we can say that customer have ambivalent satisfaction levels '),
                                                        html.Li("From exec_eff_score and prod_score we can say they don't show the interset on buying bank products."),
                                                    ])
                                                ),

                                                dcc.Tab(
                                                    label='Cluster 2',
                                                    value='cluster-2',
                                                    children=html.Div(className='control-tab', children=[
                                                        html.H4(className='cluster-2', children='Observations :- '),
                                                        html.Li('Average Age :- 32 years'),
                                                        html.Li('Average Income :- 134,000 '),
                                                        html.Li('Average Loyalty :- 6 years '),
                                                        html.Li('Average Branch Frequency :- 6 times a month '),
                                                        html.Li('Average ATM Frequency : 14 times a month'),
                                                        html.Li('Average Internet Frequency : 24 time in a month'),
                                                        html.Li('From cust_care_score, complaints_score we can say that they are satified with banks but val_for_money_score score tells that are not much happy as compare to change the bank. So it is ambivalent satisfaction level.'),
                                                        html.Li("It seems like they are busy person who have lots of internet transaction, but less time to understand the product."),
                                                    ])
                                                ),

                                                dcc.Tab(
                                                    label='Cluster 3',
                                                    value='cluster-3',
                                                    children=html.Div(className='control-tab', children=[
                                                        html.H4(className='cluster-3', children='Observations :- '),
                                                        html.Li('Average Age :-  50 years '),
                                                        html.Li('Average Income :- 290,000'),
                                                        html.Li('Average Loyalty :- 13 years  '),
                                                        html.Li('Average Branch Frequency :-  5 times a month '),
                                                        html.Li('Average ATM Frequency : 7 times a month '),
                                                        html.Li('Average Internet Frequency :  2 time in a month'),
                                                        html.Li('From other attributes we can tell they are happy with quality of their services and products of the banks'),
                                                    ])
                                                ),

                                                dcc.Tab(
                                                    label='Cluster 4',
                                                    value='cluster-4',
                                                    children=html.Div(className='control-tab', children=[
                                                        html.H4(className='cluster-4', children='Observations :- '),
                                                        html.Li('Average Age :-  30 years '),
                                                        html.Li('Average Income :- 75,000 '),
                                                        html.Li('Average Loyalty :- 5 years '),
                                                        html.Li('Average Branch Frequency :-  3 times a month'),
                                                        html.Li('Average ATM Frequency : 7 times a month '),
                                                        html.Li('Average Internet Frequency :  1 times a month '),
                                                        html.Li('From cust_care_score, complaints_score, val_for_money_score we can say that customer have Satisified by the bank services.'),
                                                        html.Li('Moreover, from exec_eff_score and prod_score we can assume that they try to understand the information provided by the bank, and they are happy with the products. '),
                                                    ])
                                                ),

                                            ]
                                            )

                                        ],
                                        id="manhattan-tabs-parent"
                                    )
                                ],
                                id="cross-filter-options",
                                className="pretty_container four columns",
                            ),

                            html.Div(
                                [
                                    html.Div(
                                        [
                                            html.Div(
                                                [
                                                    html.H6(id="Cluster_text"),
                                                    html.P("Cluster 1"),
                                                    html.P("Customer DisSatisfied"),
                                                ],
                                                id="cluser1",
                                                className="mini_container",
                                            ),

                                            html.Div(
                                                [
                                                    html.H6(id="Cluster_text"),
                                                    html.P("Cluster 2"),
                                                    html.P("Customer Satisfied"),
                                                ],
                                                id="cluser2",
                                                className="mini_container",
                                            ),

                                            html.Div(
                                                [
                                                    html.H6(id="Cluster_text"),
                                                    html.P("Cluster 3"),
                                                    html.P("Aged, Loyal Customer"),
                                                ],
                                                id="cluser3",
                                                className="mini_container",
                                            ),

                                            html.Div(
                                                [
                                                    html.H6(id="Cluster_text"),
                                                    html.P("Cluster 4"),
                                                    html.P("Satisfied Young Customer"),
                                                ],
                                                id="cluser4",
                                                className="mini_container",
                                            ),

                                        ],
                                        id="info-container",
                                        className="row container-display"
                                    ),
                                    html.Div(
                                        [

                                            html.H4(
                                                    "Cluster Discriptions"
                                                ),
                                            #dcc.Graph(id="main_graph",figure=fig)
                                            dash_table.DataTable(
                                                id='table',
                                                columns=[{"name": i, "id": i} for i in dfc.columns[1:]],
                                                data=dfc.to_dict('records'),
                                                style_table={'height': '300px', 'overflowY': 'auto', 'width':'100%'},
                                                )
                                        ],
                                        id="countGraphContainer",
                                        className="pretty_container",
                                        style={"width":"100%"}
                                    )

                                ],
                                id="right-column",
                                className="eight columns"
                            )

                        ],
                        className="row flex-display"
                    ),
                ],
                id="mainContainer",
                style={"display": "flex", "flex-direction": "column"}
            )
        ]
    )
