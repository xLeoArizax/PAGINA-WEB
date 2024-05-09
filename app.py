import dash
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import datetime

from fronted.encabezado.logo import logo, nombre
from fronted.foto.fot import picture
from fronted.graficas.graf import grafica

# Estructura de datos para almacenar los datos ingresados
datos_ingresados = []

#Se definen datos base
gravedad = 9.81  
y = 1.0  # Valor de y (altura crítica) para calcular la altura crítica inicialmente


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])


app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Sistema de Monitoreo de Fluido"), md=12),
        dbc.Col(nombre, md=10, style={'background-color': 'lightblue'})
    ]),

    html.Hr(),

    html.Div([
        html.H3("Introduzca la base del canal: "),
        dcc.Input(id='base-input', type='number', value=0),
        html.Br(),
        html.H3("Introduzca el caudal del fluido: "),
        dcc.Input(id='caudal-input', type='number', value=0),
        html.Br(),
        html.H3("Introduzca el talud del canal: "),
        dcc.Input(id='talud-input', type='number', value=0),
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






# Callback para agregar los datos a la tabla y a la lista de datos ingresados
@app.callback(
    Output('tabla-container', 'children'),
    [Input('agregar-btn', 'n_clicks')],
    [State('base-input', 'value'),
     State('caudal-input', 'value'),
     State('talud-input', 'value')]
)
def agregar_datos(n_clicks, base, caudal, taludc):
    if n_clicks > 0:
        
        hora_actual = datetime.datetime.now().strftime('%H:%M:%S')
        datos_ingresados.append({'Base': base, 'Caudal': caudal, 'Talud': taludc, 'Hora': hora_actual})
        
        # Crear una lista para almacenar las filas de la tabla
        filas_tabla = []
        
        for dato in datos_ingresados:
            # Calcular la altura crítica para cada dato ingresado
            altura_critica = (gravedad * (dato['Talud'] * y*2 + dato['Base'] * y) * (2 * dato['Talud'] * y + dato['Base']) - dato['Caudal']*2) / (2 * gravedad * (dato['Talud'] * y + dato['Base']))
            
            # Calcular el área para cada dato ingresado
            area = calcular_area(dato['Talud'], dato['Base'], altura_critica)
            
            # Calcular la velocidad para cada dato ingresado
            velocidad = calcular_velocidad(dato['Caudal'], area)
            
            # Convertir la velocidad a notación científica
            velocidad_cientifica = "{:.2e}".format(velocidad)
            
            # Agregar una nueva fila a la tabla con los datos calculados
            nueva_fila = html.Tr([
                html.Td(f"{dato['Base']:.2f}"),
                html.Td(f"{dato['Caudal']:.2f}"),
                html.Td(f"{dato['Talud']:.2f}"),
                html.Td(f"{altura_critica:.2f}"),
                html.Td(f"{area:.2f}"),
                html.Td(velocidad_cientifica),
                html.Td(dato['Hora'])
            ])
            filas_tabla.append(nueva_fila)
        
        # Crear la tabla con todas las filas
        tabla = html.Table([
            html.Thead(html.Tr([html.Th("Base"), html.Th("Caudal"), html.Th("Talud"), html.Th("Altura Crítica"), html.Th("Área"), html.Th("Velocidad"), html.Th("Hora")])),
            html.Tbody(filas_tabla)
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
                html.H3(f"La velocidad calculada es: {velocidad_cientifica}"),
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
    app.run_server(debug=True)
