# -- ------------------------------------------------------------------------------------ -- #
# -- proyecto: Microestructura y Sistemas de Trading - Laboratorio 2 - Behavioral Finance
# -- archivo: main.py - codigo principal del proyecto
# -- mantiene: IF Manuel Pintado
# -- repositorio: https://github.com/manuelpintado/LAB_2_MPD.git
# -- ------------------------------------------------------------------------------------ -- #

import funciones as fn

datos = fn.f_leer_archivo(param_archivo='reporte_cuenta.xlsx')

pip_size = fn.f_pip_size(param_ins='usdmxn')

datos = fn.f_columnas_tiempos(param_data=datos)

datos = fn.f_columnas_pips(param_data=datos)

