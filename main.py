# -- ------------------------------------------------------------------------------------ -- #
# -- proyecto: Microestructura y Sistemas de Trading - Laboratorio 2 - Behavioral Finance
# -- archivo: main.py - codigo principal del proyecto
# -- mantiene: IF Manuel Pintado
# -- repositorio: https://github.com/manuelpintado/LAB_2_MPD.git
# -- ------------------------------------------------------------------------------------ -- #

import funciones as fn

datos = fn.f_leer_archivo(param_archivo='archivo_tradeview_1.xlsx', sheet_name='Hoja1')

pip_size = fn.f_pip_size(param_ins='usdmxn')

datos = fn.f_columnas_tiempos(param_data=datos)

datos = fn.f_columnas_pips(param_data=datos)

estadisticos_ba = fn.f_estadisticas_ba(param_data=datos)

estadisticos_mad = fn.f_estadisticas_mad(param_data=datos)

