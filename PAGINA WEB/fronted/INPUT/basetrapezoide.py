import dash
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, external_stylesheets= [dbc.themes.BOOTSTRAP])

base = dbc.Container([   
    html.H2("Introduzca la base del canal: "),
    dcc.Input(id='base-input', type='number', value=0),
    html.Div(id='output-container')
])

@app.callback(
    Output('output-container', 'children'),
    [Input('base-input', 'value')]
)
def update_output(value):
    return html.H3(f"La base es: {value} m")
