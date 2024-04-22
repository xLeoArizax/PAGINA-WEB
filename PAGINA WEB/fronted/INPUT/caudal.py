import dash
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, external_stylesheets= [dbc.themes.BOOTSTRAP])

caudalt = dbc.Container([   
    html.H3("Introduzca la caudal del fluido: "),
    dcc.Input(id='caudal-input', type='number', value=0),
    html.Div(id='output-container-caudal')
])

@app.callback(
    Output('output-container-caudal', 'children'),
    [Input('caudal-input', 'value')]
)
def update_output(value):
    return html.H3(f"El caudal es: {value} m3/s")
