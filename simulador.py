#!/usr/bin/env python
#-*-coding:utf-8-*-

# 5 algoritmos
# FCFS/FIFO
# SJF No expulsivo
# SJF Expulsivo
# Round Robin
# No expulsivo por prioridades
"""
Podría usar zip...
http://www.forosdelweb.com/f130/faqs-python-591053/#post3003469
Generando por separado listas de cada "elemento" necesario. i.e. Una lista ordinal para identificar al proceso,
una lista con los tiempos de llegada, una lista con los tiempos de ráfaga, y una lista para las prioridades.
"""


# La diferencia entre el tiempo mas grande y el mas pequeño
# no debe ser mayor al tiempo de llegada del primer proceso 
# más dos veces el numero de procesos.

# xr1 - xr0 <= xt0 + np

import random
procesos = []
random.seed()

def main():
	global procesos
        cantidad_de_procesos = random.randint(1, 50)
	# Inicializar la lista de procesos
	for x in range(cantidad_de_procesos):
		# [numero proceso , tiempo llegada , rafaga de cpu , prioridad ]
		procesos.append([x, 0, random.randint(2,100), random.randint(0,10)])
	# Meterle los tiempos de llegada sin que se repitan
	# Compresión de listas | Ver detalles al final del documento
	#nuevos_tiempos_de_llegada = [ d.setdefault(x,x) for x in [random.randint(0,200) for x in range(cantidad_de_procesos ** 2)] if x not in d ]
	nuevos_tiempos_de_llegada = [d.setdefault(x,x) for d in [{}] for x in [random.randint(0,200) for y in range(cantidad_de_procesos ** 2)] if x not in d]
	#[ d.setdefault(x,x) for d in [{}] for x in startList if x not in d ]
	# Inserta los nuevos tiempos.
	for x in range(cantidad_de_procesos):
		procesos[x][1] = nuevos_tiempos_de_llegada[x]
	for x in procesos:
		print x
	#print "\n",nuevos_tiempos_de_llegada[:cantidad_de_procesos]
        r = raw_input("¿Desea aplicar el algoritmo FIFO(FCFS)?")
        if "y" in r.lower() or "s" in r.lower():
            algoritmo_fifo(True)  # Envía True para que la función se encargue de mostrar en pantalla los procesos ordenados por tiempo de llegada..
        else:
            procesos_ordenados_x_llegada = algoritmo_fifo(False)  # Envía False para que la función no muestre en pantalla los procesos ordenados por tiempo de llegada, en cambio, sólo los almacena en la variable, para usarlos en otra función más adelante.
        r = raw_input("¿Desea aplicar el algoritmo SFJ[No expulsivo]?")
        if "y" in r.lower() or "s" in r.lower():
            algoritmo_sjf(procesos_ordenados_x_llegada)  # Envía la lista de procesos, ordenados por tiempo de llegada.

def algoritmo_fifo(r):
    global procesos
    numero_procesos_llegada = []
    procesos_ordenados_x_llegada = {}
    for each_process in procesos:
        numero_procesos_llegada.append(each_process[1])
        procesos_ordenados_x_llegada[each_process[1]] = each_process
    numero_procesos_llegada.sort()
    if r:
        for x in numero_procesos_llegada:
            print procesos_ordenados_x_llegada[x]
    return procesos_ordenados_x_llegada

#export PATH='/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games'

def algoritmo_sjf(w,y):
    #global procesos
    #np = []
    #jp = {}
    jp = w
    np = y

    for each_process in procesos[1:]:
        np.append(each_process[2])
        jp[each_process[2]] = each_process
    np.sort()
    np.insert(0,procesos[0][2])
    jp[procesos[0][2]] = procesos[0]
    print np
    for x in np:
        print jp[x]
# Hasta aquí imprime claves duplicadas, debido a que las ráfagas de cpu sí se pueden repetir. Necesariob corregir.
    """np.sort()
    np.insert(0,procesos[0][2])
    print np
    for x in range(len(procesos)):
        for u in np:
            print procesos[x].index(u)"""


if __name__ == '__main__':
	main()

"""
Notas
Números son repetición

startList = [5,1,2,1,3,4,2,5,3,4]
d = {}
[ d.setdefault(x,x) for x in startList if x not in d ] [5, 1, 2, 3, 4]

And for the 'I must do it on one line' freaks, here's the single expression
variant of the above: :^)
[ d.setdefault(x,x) for d in [{}] for x in startList if x not in d ]
-----------------------------------------------------------------------------
"""
