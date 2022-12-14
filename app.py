from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
from datetime import date
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import data
import os

def load_data(date):
    status, text = data.stash_data(date, local=False)
    if status == "Error":
        return {}, [], text
    df = pd.read_csv(text)
    df = df.query("Datatype == 'calculated_current_price'")
    df = df.drop(['Datatype'], axis=1)
    df = df.drop(['Portfolio'], axis=1)
    df.reindex()
    col_names = df.columns[2:]
    return df, col_names, ""


app = Dash(__name__, external_stylesheets=[dbc.themes.LUMEN])
server = app.server

dt = date.today()
start_date = str(dt.year) + str(dt.month).zfill(2) + str(dt.day).zfill(2)

df, col_names, status = load_data(start_date)

app.layout = dbc.Container([
        dbc.Row(
            dbc.Col(
                html.Div("Trading Time Series", 
                    className="text-center",
                    style={"font-weight": "bold", "font-size": "40px"} 
                ), width=12,
            ),
        ),
        dbc.Row(
            dbc.Col(
                dbc.Container(className="text-center",children=[
                    #html.Div("Test Div", style={"background-color":"yellow","margin-left":"auto", "margin-right":"auto"}
                    dcc.DatePickerSingle(
                        id='date_id',
                        min_date_allowed=date(2022, 1, 1),
                        max_date_allowed=date.today(),
                        initial_visible_month=date.today(),
                        date=date.today()
                    )                ]
                ), width=12,
            ),
        ),

    dcc.Graph(id="graph"),
    html.Div([
            html.P(id = "status",
            children=[status])
            ]),
                                    
])

@app.callback(
    Output(component_id="graph", component_property="figure"),
    Output("status", "children"),
    Input(component_id="date_id", component_property="date"))

def update_line_chart(value):
    date = value[:4] + value[5:7] + value[8:10]
    print("about to load data for ", date)
    df = None
    col_names = None
    df, col_names, status = load_data(date)   

    print("got data for " + date)
    user = os.getlogin()
    print(df)
    if len(df) == 0:
        return {}, status
    fig = px.line(df, x="Time", y=col_names, 
            title= user + '\'s Cool Line Graph')
    fig.update_traces()
    return fig, status

app.run_server(debug=True)
#app.run()