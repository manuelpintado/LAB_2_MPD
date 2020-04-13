# -- ------------------------------------------------------------------------------------ -- #
# -- proyecto: Microestructura y Sistemas de Trading - Laboratorio 2 - Behavioral Finance
# -- archivo: funciones.py - funciones utilizadas en el proyecto
# -- mantiene: IF Manuel Pintado
# -- repositorio: https://github.com/manuelpintado/LAB_2_MPD.git
# -- ------------------------------------------------------------------------------------ -- #

import numpy as np  # funciones numericas
from datetime import timedelta  # diferencia entre datos tipo tiempo
import oandapyV20.endpoints.instruments as instruments  # informacion de precios historicos
import pandas as pd  # manejo de datos
from oandapyV20 import API  # conexion con broker OANDA
from statistics import median
from datos import token as oa_ak  # Importar token para API de OANDA
from datetime import datetime
import visualizaciones as vs  # archivo de visualizaciones para graficar


# -- --------------------------------------------------------- FUNCION: Descargar precios -- #
# -- Descargar precios historicos con OANDA

def f_precios_masivos(p0_fini, p1_ffin, p2_gran, p3_inst, p4_oatk, p5_ginc):
    """
    Funcion para descargar precios historicos masivos de OANDA

    Parameters
    ----------
    p0_fini
    p1_ffin
    p2_gran
    p3_inst
    p4_oatk
    p5_ginc
    Returns
    -------
    dc_precios
    Debugging
    ---------
    """

    def f_datetime_range_fx(p0_start, p1_end, p2_inc, p3_delta):
        """
        Parameters
        ----------
        p0_start
        p1_end
        p2_inc
        p3_delta
        Returns
        -------
        ls_resultado
        Debugging
        ---------
        """

        ls_result = []
        nxt = p0_start

        while nxt <= p1_end:
            ls_result.append(nxt)
            if p3_delta == 'minutes':
                nxt += timedelta(minutes=p2_inc)
            elif p3_delta == 'hours':
                nxt += timedelta(hours=p2_inc)
            elif p3_delta == 'days':
                nxt += timedelta(days=p2_inc)

        return ls_result

    # inicializar api de OANDA

    api = API(access_token=p4_oatk)

    gn = {'S30': 30, 'S10': 10, 'S5': 5, 'M1': 60, 'M5': 60 * 5, 'M15': 60 * 15,
          'M30': 60 * 30, 'H1': 60 * 60, 'H4': 60 * 60 * 4, 'H8': 60 * 60 * 8,
          'D': 60 * 60 * 24, 'W': 60 * 60 * 24 * 7, 'M': 60 * 60 * 24 * 7 * 4}

    # -- para el caso donde con 1 peticion se cubran las 2 fechas
    if int((p1_ffin - p0_fini).total_seconds() / gn[p2_gran]) < 4999:

        # Fecha inicial y fecha final
        f1 = p0_fini.strftime('%Y-%m-%dT%H:%M:%S')
        f2 = p1_ffin.strftime('%Y-%m-%dT%H:%M:%S')

        # Parametros pra la peticion de precios
        params = {"granularity": p2_gran, "price": "M", "dailyAlignment": 16, "from": f1,
                  "to": f2}

        # Ejecutar la peticion de precios
        a1_req1 = instruments.InstrumentsCandles(instrument=p3_inst, params=params)
        a1_hist = api.request(a1_req1)

        # Para debuging
        # print(f1 + ' y ' + f2)
        lista = list()

        # Acomodar las llaves
        for i in range(len(a1_hist['candles']) - 1):
            lista.append({'TimeStamp': a1_hist['candles'][i]['time'],
                          'Open': a1_hist['candles'][i]['mid']['o'],
                          'High': a1_hist['candles'][i]['mid']['h'],
                          'Low': a1_hist['candles'][i]['mid']['l'],
                          'Close': a1_hist['candles'][i]['mid']['c']})

        # Acomodar en un data frame
        r_df_final = pd.DataFrame(lista)
        r_df_final = r_df_final[['TimeStamp', 'Open', 'High', 'Low', 'Close']]
        r_df_final['TimeStamp'] = pd.to_datetime(r_df_final['TimeStamp'])
        r_df_final['Open'] = pd.to_numeric(r_df_final['Open'], errors='coerce')
        r_df_final['High'] = pd.to_numeric(r_df_final['High'], errors='coerce')
        r_df_final['Low'] = pd.to_numeric(r_df_final['Low'], errors='coerce')
        r_df_final['Close'] = pd.to_numeric(r_df_final['Close'], errors='coerce')

        return r_df_final

    # -- para el caso donde se construyen fechas secuenciales
    else:

        # hacer series de fechas e iteraciones para pedir todos los precios
        fechas = f_datetime_range_fx(p0_start=p0_fini, p1_end=p1_ffin, p2_inc=p5_ginc,
                                     p3_delta='minutes')

        # Lista para ir guardando los data frames
        lista_df = list()

        for n_fecha in range(0, len(fechas) - 1):

            # Fecha inicial y fecha final
            f1 = fechas[n_fecha].strftime('%Y-%m-%dT%H:%M:%S')
            f2 = fechas[n_fecha + 1].strftime('%Y-%m-%dT%H:%M:%S')

            # Parametros pra la peticion de precios
            params = {"granularity": p2_gran, "price": "M", "dailyAlignment": 16, "from": f1,
                      "to": f2}

            # Ejecutar la peticion de precios
            a1_req1 = instruments.InstrumentsCandles(instrument=p3_inst, params=params)
            a1_hist = api.request(a1_req1)

            # Para debuging
            print(f1 + ' y ' + f2)
            lista = list()

            # Acomodar las llaves
            for i in range(len(a1_hist['candles']) - 1):
                lista.append({'TimeStamp': a1_hist['candles'][i]['time'],
                              'Open': a1_hist['candles'][i]['mid']['o'],
                              'High': a1_hist['candles'][i]['mid']['h'],
                              'Low': a1_hist['candles'][i]['mid']['l'],
                              'Close': a1_hist['candles'][i]['mid']['c']})

            # Acomodar en un data frame
            pd_hist = pd.DataFrame(lista)
            pd_hist = pd_hist[['TimeStamp', 'Open', 'High', 'Low', 'Close']]
            pd_hist['TimeStamp'] = pd.to_datetime(pd_hist['TimeStamp'])

            # Ir guardando resultados en una lista
            lista_df.append(pd_hist)

        # Concatenar todas las listas
        r_df_final = pd.concat([lista_df[i] for i in range(0, len(lista_df))])

        # resetear index en dataframe resultante porque guarda los indices del dataframe pasado
        r_df_final = r_df_final.reset_index(drop=True)
        r_df_final['Open'] = pd.to_numeric(r_df_final['Open'], errors='coerce')
        r_df_final['High'] = pd.to_numeric(r_df_final['High'], errors='coerce')
        r_df_final['Low'] = pd.to_numeric(r_df_final['Low'], errors='coerce')
        r_df_final['Close'] = pd.to_numeric(r_df_final['Close'], errors='coerce')

        return r_df_final


# -- --------------------------------------------------------- FUNCION: Leer archivo excel -- #

def f_leer_archivo(param_archivo, sheet_name='Sheet1'):
    """
    Funcion para leer archivo en formato xlsx.

    :param param_archivo: Cadena de texto con el nombre del archivo
    :param sheet_name: Cadena de texto con el nombre de la hoja del archivo
    :return: dataframe de datos importados de archivo excel

    Debugging
    ---------
    param_archivo = 'archivo_tradeview_1.xlsx'
    """

    # Leer archivo
    df_data = pd.read_excel('archivos/' + param_archivo, sheet_name=sheet_name)

    # Convertir en minusculas los titulos de las columnas
    df_data.columns = [list(df_data.columns)[i].lower()
                       for i in range(0, len(df_data.columns))]

    # Elegir renglones type == buy | type == sell
    df_data = df_data[df_data.type != 'balance']

    # Resetear indice
    df_data = df_data.reset_index()

    # Asegurar ciertas columnas de tipo numerico
    numcols = ['s/l', 't/p', 'commission', 'openprice', 'closeprice', 'profit', 'size', 'swap', 'taxes', 'order']
    df_data[numcols] = df_data[numcols].apply(pd.to_numeric)

    return df_data


# -- -------------------------------- FUNCION: Diccionario de instrumentos y tamaño del pip -- #

def f_pip_size(param_ins):
    """
    Diccionario conteniendo el tamaño del multiplicador del pip para los diferentes pares de divisas.

    :param param_ins: instrumento que se busca
    :return: pips de instrumento

    Dwbugging
    ---
    param_inst = 'usdmxn'
    """

    # encontrar y eliminar _
    # inst = param_ins.replace('_', '')

    # transformar a minusculas
    param_ins = param_ins.lower()

    # lista de pips por instrumento
    pips_inst = {'eurusd': 10000,
                 'usdjpy': 100,
                 'eurjpy': 100,
                 'audusd': 10000,
                 'gbpusd': 10000,
                 'usdchf': 10000,
                 'audjpy': 100,
                 'euraud': 10000,
                 'eurgbp': 10000,
                 'gbpjpy': 100,
                 'usdcad': 10000,
                 'audcad': 10000,
                 'eurcad': 10000,
                 'gbpaud': 10000,
                 'usdhkd': 10000,
                 'gbphkd': 10000,
                 'cadhkd': 10000,
                 'usdmxn': 10000,
                 'xauusd': 10,
                 'btcusd': 1}
    return pips_inst[param_ins]


# -- ---------------------------------- FUNCION: Calcular el tiempo de una posición abierta -- #


def f_columnas_tiempos(param_data):
    """
    Funcion para encontrar el tiempo entre la apertura y cierre de una operacion en segundos.

    :param param_data: dataframe conteniendo por lo menos las columnas 'closetime' y 'opentime'
    :return: dataframe ingresado mas columna 'time' que es diferencia entre close y open

    Debugging
    --------
    param_data = datos
    """

    # convertir columna de 'closetime' y 'opentime' utilizando pd.to_datetime
    param_data['closetime'] = pd.to_datetime(param_data['closetime'])
    param_data['opentime'] = pd.to_datetime(param_data['opentime'])

    # tiempo transcurrido de una operacion
    param_data['tiempo'] = [(param_data.loc[i, 'closetime'] - param_data.loc[i, 'opentime']).delta / 1e9
                            for i in param_data.index]

    return param_data


# -- ------------------------------------------ FUNCION: Perdida/ganacia experesada en pips -- #


def f_columnas_pips(param_data, init_invest=5000):
    """
    Funcion para calcular la perdida o ganancia expresada en pips.

    :param init_invest: initial investment
    :param param_data: dataframe conteniendo por lo menos el precio de apertura, cierre y symbolo de activo
    :return: dataframe agregando columnas de diferencia de ganacia o perdida expresada en pips, pips acumulados
    del dataframe completo y

    Debugging
    --------
    param_data = datos
    """

    # calcular ganancia o perdida expresada en pips
    param_data['pips'] = [
        (param_data.loc[i, 'closeprice'] - param_data.loc[i, 'openprice']) * f_pip_size(param_data.loc[i, 'symbol'])
        if param_data.loc[i, 'type'] == 'buy'
        else (param_data.loc[i, 'openprice'] - param_data.loc[i, 'closeprice']) * f_pip_size(
            param_data.loc[i, 'symbol'])
        for i in param_data.index
    ]

    # calcular los pips acumulados de perdidas o ganancias
    param_data['pips_acum'] = param_data['pips'].cumsum()

    # calcular la ganancia o perdida acumulada de la cuenta
    param_data['profit_acum'] = param_data['profit'].cumsum()

    # calcular el capital acumulado por operacion
    param_data['capital_acum'] = [init_invest + param_data['profit_acum'][i] for i in param_data.index]

    return param_data


# -- -------------------------------------------------------- FUNCION: Estadisticas basicas -- #


def f_estadisticas_ba(param_data, ver_grafica=False):
    """

    :param param_data: Dataframe conteniendo las operaciones realizadas en la cuenta
    :param ver_grafica: booleano para mostrar grafica de pastel del ranking
    :return: Diccionario conteniendo 2 dataframes:
                1. Concentrado de las estadisticas basicas de la cuenta
                2. ranking de los activos utilizados (% de ganadas/perdidas por cada activo utilizado)

    Debugging
    --------
    param_data = datos

    """

    # lista de medidas
    medidas = np.array(['Ops totales',
                        'Ganadoras',
                        'Ganadoras_c',
                        'Ganadoras_v',
                        'Perdedoras',
                        'Perdedoras_c',
                        'Perdedoras_v',
                        'Media (Profit)',
                        'Media (Pips)',
                        'r_efectividad',
                        'r_proporcion',
                        'r_efectividad_c',
                        'r_efectividad_v'])

    # lista de descripciones de diferentes indices de dataframe
    descripciones = np.array(['Operaciones totales',
                              'Operaciones ganadoras',
                              'Operaciones ganadoras de compra',
                              'Operaciones ganadoras de venta',
                              'Operaciones perdedoras',
                              'Operaciones perdedoras de compra',
                              'Operaciones perdedoras de venta',
                              'Mediana de profit de operaciones',
                              'Mediana de pips de operaciones',
                              'Operaciones Totales Vs Ganadoras Totales',
                              'Ganadoras Totales Vs Perdedoras Totales',
                              'Totales Vs Ganadoras Compras',
                              'Totales Vs Ganadoras Ventas'])
    # crear dataframe
    df_1_tabla = pd.DataFrame(columns=['medidas', 'valor'],
                              index=np.array([i for i in range(0, len(medidas))]))

    # Llenar medidas
    df_1_tabla['medidas'] = [medidas[i] for i in range(0, len(df_1_tabla.index))]

    # Llenar descripciones
    df_1_tabla['descripcion'] = [descripciones[i] for i in range(0, len(df_1_tabla.index))]

    # llenado de informacion
    df_1_tabla.loc[0, 'valor'] = len(param_data.index)
    df_1_tabla.loc[1, 'valor'] = sum(1 for i in param_data.index if param_data.loc[i, 'profit'] >= 0)
    df_1_tabla.loc[2, 'valor'] = sum(1 for i in param_data.index if param_data.loc[i, 'profit'] >= 0 and
                                     param_data.loc[i, 'type'] == 'buy')
    df_1_tabla.loc[3, 'valor'] = sum(1 for i in param_data.index if param_data.loc[i, 'profit'] >= 0 and
                                     param_data.loc[i, 'type'] == 'sell')
    df_1_tabla.loc[4, 'valor'] = sum(1 for i in param_data.index if param_data.loc[i, 'profit'] < 0)
    df_1_tabla.loc[5, 'valor'] = sum(1 for i in param_data.index if param_data.loc[i, 'profit'] < 0 and
                                     param_data.loc[i, 'type'] == 'buy')
    df_1_tabla.loc[6, 'valor'] = sum(1 for i in param_data.index if param_data.loc[i, 'profit'] < 0 and
                                     param_data.loc[i, 'type'] == 'sell')
    df_1_tabla.loc[7, 'valor'] = np.round(median(param_data['profit']), 3)
    df_1_tabla.loc[8, 'valor'] = np.round(median(param_data['pips']), 3)
    df_1_tabla.loc[9, 'valor'] = np.round(df_1_tabla.loc[0, 'valor'] /
                                          df_1_tabla.loc[1, 'valor'], 2)
    df_1_tabla.loc[10, 'valor'] = np.round(df_1_tabla.loc[1, 'valor'] /
                                           df_1_tabla.loc[4, 'valor'], 2)
    df_1_tabla.loc[11, 'valor'] = np.round(df_1_tabla.loc[0, 'valor'] /
                                           df_1_tabla.loc[2, 'valor'], 2)
    df_1_tabla.loc[12, 'valor'] = np.round(df_1_tabla.loc[0, 'valor'] /
                                           df_1_tabla.loc[3, 'valor'], 2)

    # simbolos del dataframe
    symbols = np.unique(param_data.symbol)

    # creating ranking dataframe
    df_2_ranking = pd.DataFrame(columns=['symbol', 'rank'],
                                index=np.array([i for i in range(0, len(symbols))]))

    # fill symbols
    df_2_ranking['symbol'] = [symbols[i] for i in range(0, len(symbols))]

    # ranking
    i = 0
    for symbol in symbols:
        ganadas = sum(1 for i in param_data.index
                      if param_data.loc[i, 'profit'] >= 0 and param_data.loc[i, 'symbol'] == symbol)
        totales = sum(1 for i in param_data.index if param_data.loc[i, 'symbol'] == symbol)

        df_2_ranking.loc[i, 'rank'] = str(np.round(ganadas / totales * 100, 2)) + '%'
        i += 1

    # create the dictionary

    final_dict = {'df_1_tabla': df_1_tabla, 'df_2_ranking': df_2_ranking}

    if ver_grafica:
        vs.g_pastel(p0_dict=final_dict)

    return final_dict


# -- ---------------------------------------------------- FUNCION: Calcular Ganancias o Perdidas diarias -- #


def f_profit_diario(param_data, init_invest=5000):
    """

    :param param_data: Dataframe con columna opentime
    :param init_invest: inversion inicial del portafolio
    :return: DataFrame diario

    Debugging
    --------
    param_data = datos

    """
    daily = param_data[['closetime', 'profit']]
    daily.rename(columns={'closetime': 'timestamp', 'profit': 'profit_d'}, inplace=True)
    daily.index = daily.timestamp
    daily = daily.resample("d").sum().reset_index()
    # calcular la ganancia o perdida acumulada de la cuenta
    daily['profit_acm_d'] = daily['profit_d'].cumsum() + init_invest

    return daily


# -- ---------------------------------------------------- FUNCION: Estadisticas financieras -- #


def f_estadisticas_mad(param_data, rf=0.08 / 300, mar=.3 / 300, ver_grafica=False):
    """

    :param param_data: Dataframe de informacion cuenta de trading
    :param rf: tasa libre de risgo, base = 8%
    :param mar: base 30%
    :param ver_grafica: Booleano para ver grafica de lina de capital acumulado con DrawDown y DrawUp
    :return: Data Frame de estadisticas financieras

    Debugging
    --------
    param_data = datos
    """

    # medidas de atribucion al desempeño (mad)
    mad = np.array(['sharpe',
                    'sortino_c',
                    'sortino_v',
                    'drawdown_capi',
                    'drawup_capi',
                    'information_r'])

    # descripciones de las mad
    descripciones = np.array(['Sharpe Ratio',
                              'Sortino Ratio para Posiciones  de Compra',
                              'Sortino Ratio para Posiciones de Venta',
                              'DrawDown de Capital',
                              'DrawUp de Capital',
                              'Informatio Ratio'])

    # creacion de dataframe de mad
    df_mad = pd.DataFrame(columns=['metrica', 'valor', 'descripcion'],
                          index=np.array([i for i in range(0, len(mad))]))

    # Llenar medidas
    df_mad['metrica'] = [mad[i] for i in range(0, len(df_mad.index))]

    # Llenar descripciones
    df_mad['descripcion'] = [descripciones[i] for i in range(0, len(df_mad.index))]

    # Data Frame de datos diarios
    daily = f_profit_diario(param_data)
    daily_buy = f_profit_diario(param_data[param_data.type == 'buy'])
    daily_sell = f_profit_diario(param_data[param_data.type == 'sell'])

    # calculo de las diferentes mad

    # sharp ratio
    returns = np.log(daily.profit_acm_d / daily.profit_acm_d.shift()).dropna()
    port_log_ret = np.sum(returns)
    port_std = returns.std()
    df_mad.valor[0] = (port_log_ret - rf) / port_std

    # sortino_c
    returns_buy = np.log(daily_buy.profit_acm_d / daily_buy.profit_acm_d.shift()).dropna()
    port_std_buy = np.std(np.array([ret for ret in returns_buy if ret < mar]))
    df_mad.valor[1] = (np.sum(returns_buy) - mar) / port_std_buy

    # sortino_v
    returns_sell = np.log(daily_sell.profit_acm_d / daily_sell.profit_acm_d.shift()).dropna()
    port_std_sell = np.std(np.array([ret for ret in returns_sell if ret < mar]))
    df_mad.valor[2] = (np.sum(returns_sell) - mar) / port_std_sell

    # drawdown_capi
    df_mad.valor[3] = draw_down(daily)

    # drawup_capi
    df_mad.valor[4] = draw_up(daily)

    # information_r
    benchmark_ret = benchmark_data(param_data=param_data)
    tracking_err = returns - benchmark_ret['ret']
    df_mad.valor[5] = (port_log_ret - np.sum(benchmark_ret['ret'])) / tracking_err.std()

    # Grafica de linea con Draw Down y Draw Up
    if ver_grafica:
        vs.g_dd_du(df_data=daily, df_estadisticos=df_mad)

    return df_mad


# -- ---------------------------------------------------- FUNCION: Draw Down -- #

def draw_down(param_data):
    """

    :param param_data: DataFrame
    :return: string con fecha de incio, fecha de fin y monto

    Debugging
    --------
    param_data = datos_diarios

    """
    mdd = 0
    peak = param_data.profit_acm_d[0]
    start = param_data.timestamp[0]
    end = param_data.timestamp[0]
    for i in param_data.index:
        if param_data.profit_acm_d[i] > peak and end <= start:
            peak = param_data.profit_acm_d[i]
            start = param_data.timestamp[i]
        dd = peak - (param_data.profit_acm_d[i])
        if dd > mdd:
            mdd = dd
            end = param_data.timestamp[i]

    if mdd < 1:
        start = param_data.timestamp[0]
        end = param_data.timestamp[0]
    return '"' + str(start) + '" "' + str(end) + '" $' + str(mdd)


# -- ---------------------------------------------------- FUNCION: Draw Up -- #

def draw_up(param_data):
    """

    :param param_data: DataFrame
    :return: string con fecha de incio, fecha de fin y monto

    Debugging
    --------
    param_data = datos_diarios

    """
    mdu = 0
    lowest = param_data.profit_acm_d[0]
    start = param_data.timestamp[0]
    end = param_data.timestamp[0]
    for i in param_data.index:
        if param_data.profit_acm_d[i] < lowest:
            lowest = param_data.profit_acm_d[i]
            start = param_data.timestamp[i]
        du = param_data.profit_acm_d[i] - lowest
        if du > mdu:
            mdu = du
            end = param_data.timestamp[i]
    if mdu < 1:
        start = param_data.timestamp[0]
        end = param_data.timestamp[0]
    return '"' + str(start) + '" "' + str(end) + '" $' + str(mdu)


# -- ---------------------------------------------------- FUNCION: Informacion Benchmark -- #

def benchmark_data(param_data, benchmark='SPX500_USD'):
    """

    :param param_data: dataframe that includes open time and close time of operations
    :param benchmark: index that is considered the benckmark for portfolio
    :return: dataframe containing benckmarks returns

    Debugging
    --------
    param_data = datos
    benchmark='^GSPC'
    """

    fini = pd.to_datetime(param_data['opentime'].iloc[0]).tz_localize('GMT')
    fini = datetime.strptime(fini.strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
    ffin = pd.to_datetime(param_data['closetime'].iloc[-1]).tz_localize('GMT')
    ffin = datetime.strptime(ffin.strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
    granularity = "D"
    df_benchmark = f_precios_masivos(p0_fini=fini, p1_ffin=ffin, p2_gran=granularity, p3_inst=benchmark,
                                     p4_oatk=oa_ak, p5_ginc=4900)

    df_benchmark['ret'] = np.log(df_benchmark.Close / df_benchmark.Close.shift()).dropna()

    return df_benchmark


# -- ----------------------------------------------------------- FUNCION: Sesgos cognitivos -- #


def f_be_de(param_data, ver_grafica=False):
    """

    :param param_data: Data Frame con datos de la cuenta
    :param ver_grafica: booleano para visualizar grafica
    :return: diccionario con las ocurrencias de los sesgos cognitivos y estadisticos

    Debugging
    --------
    param_data = datos

    """
    # Sacar ganadora o perdedora
    param_data['status'] = ['win' if param_data.profit[i] >= 0 else 'lose'
                            for i in param_data.index]

    # ratios
    # Ratio operaciones ganadoras
    param_data["ratio_win"] = [param_data.profit[i] / param_data.capital_acum[i] * 100 if param_data.status[i] == 'win'
                               else 0 for i in param_data.index]
    # Ratio operaciones perdedoras
    param_data["ratio_lose"] = [
        param_data.profit[i] / param_data.capital_acum[i] * 100 if param_data.status[i] == 'lose'
        else 0
        for i in param_data.index]

    # crear df de operaciones ganadas y de perdidas
    winners = param_data[param_data.status == "win"]
    losers = param_data[param_data.status == "lose"]

    # inicializar variables para diccionario
    cantidad = 0
    status = 0
    aversion = 0
    sensibilidad_decreciente = 0

    # DataFrame de informacion final
    resultados = pd.DataFrame(columns=['ocurrencias', 'status_quo', 'aversion_perdida', 'sensibilidad_decreciente'],
                              index=[0])

    # Crear outline del diccionario
    diccionario = {
        'ocurrencias': {
            'cantidad': cantidad
        },
        'resultados': resultados
    }

    # Encontrar sesgos
    for i in winners.index:
        winner = winners.loc[i]
        for j in losers.index:
            loser = losers.loc[j]
            if loser.opentime < winner.closetime < loser.closetime:
                cantidad += 1
                time = winner.closetime  # cierre operacion ganadora que tiene el sesgo
                nombre = 'ocurrencia_' + str(cantidad)
                diccionario['ocurrencias'][nombre] = {
                    'timestamp': time,
                    'operaciones': {
                        'ganadora': {
                            'instrumento': winner.symbol,
                            'volumen': winner.size,
                            'sentido': winner.type,
                            'capital_ganadora': winner.profit
                        },
                        'perdedora': {
                            'instrumento': loser.symbol,
                            'volumen': loser.size,
                            'sentido': loser.type,
                            'capital_ganadora': loser.profit
                        }
                    },
                    'ratio_cp_capital_acm': loser.ratio_lose,
                    'ratio_cg_capital_acm': winner.ratio_win,
                    'ratio_cp_cg': loser.profit / winner.profit
                }
                if winner.profit / winner.capital_acum > np.abs(loser.profit / loser.capital_acum):
                    status += 1
                if np.abs(loser.profit / winner.profit) > 1.5:
                    aversion += 1
                try:
                    if winners.capital_acum[i - 1] < winners.capital_acum[i] and \
                            (winners.profit[i - 1] < winners.profit[i] or losers.profit[i - 1] < losers.profiti) and \
                            np.abs(loser.profit) / winner.profit > 1.5:
                        sensibilidad_decreciente += 1
                except IndexError:
                    sensibilidad_decreciente = sensibilidad_decreciente

    diccionario['ocurrencias']['cantidad'] = cantidad
    diccionario['resultados']['ocurrencias'][0] = cantidad
    try:
        diccionario['resultados']['status_quo'][0] = status / cantidad * 100
        diccionario['resultados']['aversion_perdida'][0] = aversion / cantidad * 100
    except ZeroDivisionError:
        diccionario['resultados']['status_quo'][0] = 0
        diccionario['resultados']['aversion_perdida'][0] = 0
    diccionario['resultados']['sensibilidad_decreciente'][0] = 'si'

    if winners.capital_acum.iloc[0] > winners.capital_acum.iloc[-1]:
        diccionario['resultados']['sensibilidad_decreciente'][0] = 'no'
    if winners.profit.iloc[0] > winners.profit.iloc[-1] and losers.profit.iloc[0] < losers.profit.iloc[-1]:
        diccionario['resultados']['sensibilidad_decreciente'][0] = 'no'
    if np.abs(losers.profit.min()) / winners.profit.max() < 1.5:
        diccionario['resultados']['sensibilidad_decreciente'][0] = 'no'

    if ver_grafica:
        vs.g_disposition(status_quo=status, aversion=aversion, sensibilidad_decreciente=sensibilidad_decreciente)

    return diccionario
