import dash
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import datetime

from fronted.encabezado.logo import logo, nombre
from fronted.foto.fot import picture
from fronted.INPUT.basetrapezoide import base
from fronted.INPUT.caudal import caudalt
from fronted.INPUT.talud import taludc





app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server : app.server

# Estructura de datos para almacenar los datos ingresados
datos_ingresados = []

#Se definen datos base
gravedad = 9.81  
y = 1.0  # Valor de y (altura crítica) para calcular la altura crítica inicialmente
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Sistema de Monitoreo de Fluido"), md=12),
        dbc.Col(nombre, md=10, style={'background-color': 'lightblue'})
    ]),

    html.Hr(),

    dbc.Col([
        dbc.Col(base),
        dbc.Col(caudalt),
        dbc.Col(taludc),
    ]),

    html.Div([
        html.Br(),
        html.Button('Agregar', id='agregar-btn', n_clicks=0),  # Botón para agregar datos
        html.Hr(),
        html.Div(id='output-container'),
        html.Hr(),
        html.Button('Limpiar', id='limpiar-btn', n_clicks=0),  # Botón para limpiar
        html.Div(id='tabla-container'),
        
        
        
    ]),

    

    html.Hr(),
    

])

# Función para calcular el área
def calcular_area(talud, base, altura_critica):
    area = talud * altura_critica**2 + base * altura_critica
    return area

# Función para calcular la velocidad
def calcular_velocidad(caudal, area):
    velocidad = caudal / area
    return velocidad






# Callback para actualizar los elementos de salida y almacenar los datos ingresados
@app.callback(
    Output('output-container', 'children'),
    [Input('base-input', 'value'),
     Input('caudal-input', 'value'),
     Input('talud-input', 'value')]
)
def update_output(base, caudal, taludc):
    return [
        html.H3(f"La base ingresada es: {base} m"),
        html.H3(f"El caudal es: {caudal} m3/s"),
        html.H3(f"El talud del canal es: {taludc}")
    ]







# Callback para agregar los datos a la tabla y a la lista de datos ingresados
@app.callback(
    Output('tabla-container', 'children'),
    [Input('agregar-btn', 'n_clicks')],
    [State('base-input', 'value'),
     State('caudal-input', 'value'),
     State('talud-input', 'value')]
)

#Agregar datos a la tabla como almacenamiento
def agregar_datos(n_clicks, base, caudal, taludc):
    if n_clicks > 0:
        
        hora_actual = datetime.datetime.now().strftime('%H:%M:%S')
        datos_ingresados.append({'Base': base, 'Caudal': caudal, 'Talud': taludc, 'Hora': hora_actual})
        
        # Calcular la altura crítica
        altura_critica = (gravedad * (taludc * y**2 + base * y) * (2 * taludc * y + base) - caudal**2) / (2 * gravedad * (taludc * y + base))
        
        # Calcular el área
        area = calcular_area(taludc, base, altura_critica)
        
        # Calcular la velocidad
        velocidad = calcular_velocidad(caudal, area)

        
        tabla = html.Table([
            html.Thead(html.Tr([html.Th("Base"), html.Th("Caudal"), html.Th("Talud"), html.Th("Altura Crítica"), html.Th("Área"), html.Th("Velocidad"), html.Th("Hora")])),
            html.Tbody([
                html.Tr([
                    html.Td(f"{dato['Base']:.2f}"),
                    html.Td(f"{dato['Caudal']:.2f}"),
                    html.Td(f"{dato['Talud']:.2f}"),
                    html.Td(f"{altura_critica:.2f}"),
                    html.Td(f"{area:.2f}"),
                    html.Td(f"{velocidad:.2f}"),
                    html.Td(dato['Hora'])
                ])
                for dato in datos_ingresados
            ])
        ], style={'background-color': 'lightyellow', 'margin': 'auto', 'text-align': 'center'}) 
        
        colores_barras = ['blue', 'red', 'green', 'orange', 'purple', 'yellow', 'cyan', 'magenta', 'lime', 'pink']

        # gráfica de barras para el caudal vs hora 
        caudal_hora_graph = dcc.Graph(
            id='caudal-hora-graph',
            figure={
                'data': [{
                    'x': [dato['Hora'] for dato in datos_ingresados],
                    'y': [dato['Caudal'] for dato in datos_ingresados],
                    'type': 'bar',
                    'name': 'Caudal',
                    'marker': {'color': colores_barras[i % len(colores_barras)]}  
                } for i, _ in enumerate(datos_ingresados)],
                'layout': {
                    'title': 'Caudal vs Hora',
                    'xaxis': {'title': 'Hora'},
                    'yaxis': {'title': 'Caudal (m3/s)'}
                }
            }
        )

        # gráfica de barras para la velocidad vs hora
        velocidad_hora_graph = dcc.Graph(
            id='velocidad-hora-graph',
            figure={
                'data': [{
                    'x': [dato['Hora'] for dato in datos_ingresados],
                    'y': [calcular_velocidad(dato['Caudal'], calcular_area(dato['Talud'], dato['Base'], altura_critica)) for dato in datos_ingresados],
                    'type': 'bar',
                    'name': 'Velocidad',
                    'marker': {'color': colores_barras[i % len(colores_barras)]}  
                } for i, _ in enumerate(datos_ingresados)],
                'layout': {
                    'title': 'Velocidad vs Hora',
                    'xaxis': {'title': 'Hora'},
                    'yaxis': {'title': 'Velocidad (m/s)'}
                }
            }
        )

        altura_critica_box = dbc.Card(
        dbc.CardBody([
            html.H3(f"La altura crítica calculada es: {altura_critica}"),
    ]),
    style={'background-color': 'lightgreen', 'margin': '10px', 'text-align': 'right'}
)

        area_box = dbc.Card(
            dbc.CardBody([
                html.H3(f"El área calculada es: {area}"),
            ]),
            style={'background-color': 'lightblue', 'margin': '10px', 'text-align': 'left'}
        )

        velocidad_box = dbc.Card(
            dbc.CardBody([
                html.H3(f"La velocidad calculada es: {velocidad}"),
            ]),
            style={'background-color': 'lightcoral', 'margin': '10px', 'text-align': 'center'}
        )

        # Agregar las gráficas y los recuadros al layout
        return tabla, dbc.Row([
            dbc.Col(altura_critica_box, md=4),
            dbc.Col(area_box, md=4),
            dbc.Col(velocidad_box, md=4)
        ]), caudal_hora_graph, velocidad_hora_graph

    

# Callback para limpiar los datos
@app.callback(
    Output('base-input', 'value'),
    Output('caudal-input', 'value'),
    Output('talud-input', 'value'),
    [Input('limpiar-btn', 'n_clicks')]
)




def limpiar_campos(n_clicks):
    if n_clicks > 0:
        datos_ingresados.clear()
        # Restablecer el valor de los campos de entrada
        return 0, 0, 0
    else:
        raise dash.exceptions.PreventUpdate


if __name__ == '__main__':
    app.run_server(debug=True, host = '0.0.0.0')
