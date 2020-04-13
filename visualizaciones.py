# -- ------------------------------------------------------------------------------------ -- #
# -- proyecto: Microestructura y Sistemas de Trading - Laboratorio 2 - Behavioral Finance
# -- archivo: visualizaciones.py - funciones para visualizar informacion del proyecto
# -- mantiene: IF Manuel Pintado
# -- repositorio: https://github.com/manuelpintado/LAB_2_MPD.git
# -- ------------------------------------------------------------------------------------ -- #

import plotly.graph_objects as go  # Libreria para graficar
import plotly.io as pio  # renderizador para visualizar imagenes
import pandas as pd  # Libreria para bases de datos
import numpy as np  # libreria para manejo de numeros

pio.renderers.default = "browser"  # render de imagenes para correr en script


# -- --------------------------------------------------------- GRÁFICA: Pastel Tickers Utilizados -- #

def g_pastel(p0_dict, title='Ranking of tickers in transactions'):
    """

    :param title: title of the graph
    :param p0_dict: dictionary containing df_1_ranking
    :return: pie chart with greatest value extracted

    Debugging
    --------
    p0_dict = estadisticos_ba

    """

    def p2f(x):
        """

        :param x: string con %
        :return: float sin % y en decimal

        Debugging
        --------
        x = "2%"
        """
        return float(x.strip('%')) / 100

    def pull_values(data):
        """

        :param data: arreglo de numpy de valores
        :return: arreglo de numpy de 0 y 0.2 en la posicion del valor mas grande de la cadena

        Debugging
        --------
        data = np.array([0, 1, 8, 3, 5, 0, 3])
        """
        largest_value = np.zeros_like(data)
        largest = data.argmax()
        largest_value[largest] = 0.2
        return largest_value

    symbols = np.array(p0_dict['df_2_ranking']['symbol'])
    values = np.array([p2f(x) for x in p0_dict['df_2_ranking']['rank']])
    pull = pull_values(values)
    fig = go.Figure()
    fig.add_trace(go.Pie(labels=symbols, values=values, pull=pull))
    fig.update_layout(title_text=title, font=dict(family="Courier New, monospace", size=18, color="#7f7f7f"),
                      showlegend=True)
    fig.show()

    return fig


# -- --------------------------------------------------------- GRÁFICA: Draw Down y Draw Up -- #

def g_dd_du(df_data, df_estadisticos):
    """

    :param df_data: Dataframe con los datos diarios del portafolio
    :param df_estadisticos: Dataframe de los estadisticos de la funcion f_estadisticos_mad
    :return: Gráfica de linea con evolucion del capital acumulado, Draw Down maximo y Draw Up

    Debugging
    --------
    df_data = datos_diarios
    df_estadisticos = estadisticos_mad
    """

    # Encontrar fechas de inicio y fin del Draw Down y Draw Up usando la funcion de estadisticos MAD
    start_dd = pd.to_datetime(df_estadisticos['valor'][3].split()[0].replace('"', ''))
    end_dd = pd.to_datetime(df_estadisticos['valor'][3].split()[2].replace('"', ''))
    start_du = pd.to_datetime(df_estadisticos['valor'][4].split()[0].replace('"', ''))
    end_du = pd.to_datetime(df_estadisticos['valor'][4].split()[2].replace('"', ''))

    # Encontrar los valores de Y para la linea de DU y DD
    df_data.index = df_data.timestamp

    # Crear gráfica
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_data.timestamp, y=df_data.profit_acm_d + 5000, name="Capital Acumulado",
                             marker_color='Black'))
    fig.add_shape(type='line', x0=start_dd, x1=end_dd,
                  y0=df_data['profit_acm_d'][start_dd] + 5000, y1=df_data['profit_acm_d'][end_dd] + 5000,
                  line=dict(color="Red", width=4, dash="dashdot"),
                  name='Maximum Draw Down')
    fig.add_shape(type='line', x0=start_du, x1=end_du,
                  y0=df_data['profit_acm_d'][start_du] + 5000, y1=df_data['profit_acm_d'][end_du] + 5000,
                  line=dict(color="Green", width=4, dash="dashdot"),
                  name='Maximum Draw Up')
    fig.update_layout(title_text='Max DrawDown and DrawUp',
                      xaxis_title="Fecha", yaxis_title="$USD",
                      font=dict(family="Courier New, monospace", size=18, color="#7f7f7f"),
                      showlegend=True)

    fig.show()

    return fig


# -- --------------------------------------------------------- GRÁFICA: Disposition Effect -- #
def g_disposition(status_quo, aversion, sensibilidad_decreciente):
    """

    :param status_quo: contador de veces que se dio el sesgo
    :param aversion: contador de veces que se dio el sesgo
    :param sensibilidad_decreciente: contador de veces que se dio el sesgo
    :return: grafica de barras con ocurrencias de cada sesgo cognitivo

    Debugging
    --------
    status_quo = 1
    aversion = 1
    sensibilidad_decreciente = 1
    """

    # crear figura
    fig = go.Figure()
    # Agregar grafica de barras a figura
    fig.add_trace(go.Bar(x=['status_quo', 'aversion_perdida', 'sensibilidad_decreciente'],
                         y=[status_quo, aversion, sensibilidad_decreciente]))
    # Agregar títulos y ejes
    fig.update_layout(title_text='Sesgos Cognitivos',
                      xaxis_title="Sesgo", yaxis_title="# de Ocurrencias",
                      font=dict(family="Courier New, monospace", size=18, color="#7f7f7f"))

    fig.show()

    return fig
