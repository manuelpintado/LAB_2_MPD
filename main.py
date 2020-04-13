# -- ------------------------------------------------------------------------------------ -- #
# -- proyecto: Microestructura y Sistemas de Trading - Laboratorio 2 - Behavioral Finance
# -- archivo: main.py - codigo principal del proyecto
# -- mantiene: IF Manuel Pintado
# -- repositorio: https://github.com/manuelpintado/LAB_2_MPD.git
# -- ------------------------------------------------------------------------------------ -- #

import funciones as fn

# Leer archivo de excel formato xlsx
datos = fn.f_leer_archivo(param_archivo='reporte_cuenta.xlsx')

# verificar funcionamiento de funcion tamaño pips
pip_size = fn.f_pip_size(param_ins='usdmxn')

# Calculos de tiempo transcurrido de operaciones
datos = fn.f_columnas_tiempos(param_data=datos)

# Calculos de pips y capital
datos = fn.f_columnas_pips(param_data=datos)

# Calculo de estadisticos basicos y ranking de portafolio
estadisticos_ba = fn.f_estadisticas_ba(param_data=datos, ver_grafica=False)

# Calculo datos diarios del portafolio
datos_diarios = fn.f_profit_diario(param_data=datos)

# Estadisticos financieros
estadisticos_mad = fn.f_estadisticas_mad(param_data=datos, ver_grafica=True)

# Sesgos
sesgos_cognitivos = fn.f_be_de(param_data=datos, ver_grafica=False)
