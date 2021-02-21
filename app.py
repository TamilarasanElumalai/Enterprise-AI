# Import required libraries
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
from pages import (
    overview
)


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}], external_stylesheets=external_stylesheets
)
server = app.server

# Describe the layout/ UI of the app
app.layout = html.Div(
    [dcc.Location(id="url", refresh=False), html.Div(id="page-content")]
)

# Update page
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    if pathname == "/customer-segmentation-report/overview":
        return overview.create_layout(app)
    else:
        return overview.create_layout(app)

if __name__ == "__main__":
    app.run_server(debug=True)
