import dash
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, external_stylesheets= [dbc.themes.BOOTSTRAP])

profundidadla = dbc.Container([   
    html.H3("Introduzca la la profundidad de la lamina de agua: "),
    dcc.Input(id='profundidad-input', type='number', value=0),
    html.Div(id='output-container-profundidad')
])

@app.callback(
    Output('output-container-profundidad', 'children'),
    [Input('profundidad-input', 'value')]
)
def update_output(value):
    return html.H3(f"El profundidad de la lamina de agua es: {value} m")