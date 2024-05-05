import dash
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, external_stylesheets= [dbc.themes.BOOTSTRAP])

base = dbc.Container([   
        html.H3("Introduzca la base del canal: "),
        dcc.Input(id='base-input', type='number', value=0),
    html.Div(id='output-container-base')
])

@app.callback(
    Output('output-container-base', 'children'),
    [Input('base-input', 'value')]
)
def update_output(value):
    return html.H3(f"El caudal es: {value} m3/s")