import dash
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, external_stylesheets= [dbc.themes.BOOTSTRAP])

lamagua = dbc.Container([   
    html.H3("Introduzca la altura de la lámina de agua: "),
    dcc.Input(id='altura-input', type='number', value=0),
    html.Div(id='output-container')
])

@app.callback(
    Output('output-container', 'children'),
    [Input('altura-input', 'value')]
)
def update_output(value):
    return html.H3(f"La altura de la lámina de agua es: {value} m")
