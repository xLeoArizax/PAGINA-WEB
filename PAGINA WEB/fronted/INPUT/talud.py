import dash
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, external_stylesheets= [dbc.themes.BOOTSTRAP])

taludc = dbc.Container([   
    html.H3("Introduzca la la talud de la lamina de agua: "),
    dcc.Input(id='talud-input', type='number', value=0),
    html.Div(id='output-container-talud')
])

@app.callback(
    Output('output-container-talud', 'children'),
    [Input('talud-input', 'value')]
)
def update_output(value):
    return html.H3(f"El talud del canal es: {value} m")