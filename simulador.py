#!/usr/bin/env python
#-*-coding:utf-8-*-

# Idea del programa:
# Implementar 5 algoritmos »
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
        cantidad_de_procesos = random.randint(2, 35)
	# Inicializar la lista de procesos
	for x in range(cantidad_de_procesos):
		# [numero proceso , tiempo llegada , rafaga de cpu , prioridad ]i
		procesos.append([x, 0, random.randint(2,10), random.randint(0,10)])
	# Meterle los tiempos de llegada sin que se repitan
	# Compresión de listas | Ver detalles al final del documento
	#nuevos_tiempos_de_llegada = [ d.setdefault(x,x) for x in [random.randint(0,200) for x in range(cantidad_de_procesos ** 2)] if x not in d ]
	nuevos_tiempos_de_llegada = [d.setdefault(x,x) for d in [{}] for x in [random.randint(0,50) for y in range(cantidad_de_procesos ** 3)] if x not in d]
	#[ d.setdefault(x,x) for d in [{}] for x in startList if x not in d ]
	# Inserta los nuevos tiempos.
	for x in range(cantidad_de_procesos):
		procesos[x][1] = nuevos_tiempos_de_llegada[x]
        acomodo(procesos)
	#print "\n",nuevos_tiempos_de_llegada[:cantidad_de_procesos]
        respuesta = raw_input("¿Desea aplicar el algoritmo FIFO(FCFS)?")
        if "y" in respuesta.lower() or "s" in respuesta.lower():
            procesos_ordenados_x_llegada = algoritmo_fifo(True)  # Envía True para que la función se encargue de mostrar en pantalla los procesos ordenados por tiempo de llegada..
        else:
            procesos_ordenados_x_llegada = algoritmo_fifo(False)  # Envía False para que la función no muestre en pantalla los procesos ordenados por tiempo de llegada, en cambio, sólo los almacena en la variable, para usarlos en otra función más adelante.
        respuesta = raw_input("¿Desea aplicar el algoritmo SFJ[No expulsivo]?")
        if "y" in respuesta.lower() or "s" in respuesta.lower():
            algoritmo_sjf(procesos_ordenados_x_llegada)  # Envía la lista de procesos, ordenados por tiempo de llegada.

def algoritmo_fifo(respuesta):
    global procesos
    respuesta = respuesta
    numero_procesos_llegada = []  # Se inicializan las variables
    procesos_ordenados_x_llegada = {}  # Se inicializan las variables
    procesos_ordenados_x_llegada2 = []  # Se inicializan las variables
    lista_nueva = []  # Se inicializan las variables
    for each_process in procesos:
        numero_procesos_llegada.append(each_process[1])
        procesos_ordenados_x_llegada[each_process[1]] = each_process
    numero_procesos_llegada.sort()
    for x in numero_procesos_llegada:
        procesos_ordenados_x_llegada2.append(procesos_ordenados_x_llegada[x])  # Añade las claves de diccionario en una lista vacía, siguiendo el orden de la lista de los tiempos de llegada(De manera ascendendete)
        lista_nueva.append(procesos_ordenados_x_llegada[x][:])
    if respuesta:
        acomodo(procesos_ordenados_x_llegada2)  # Si la respuesta es verdadera llama a la función que se encarga de mostrar en pantalla de manera ordenada.
        print "\nNomP\tLL\tRCpu\tPrior!\tTRet\tTEsp"
    lista_nueva = lista_nueva[:]
    acumulador_tiempo_ret = lista_nueva[0][1]
    acumulador_tiempo_esp = lista_nueva[0][1]
    for x in range(len(lista_nueva)):
        acumulador_tiempo_ret += lista_nueva[x][2]  # Variable para llevar el total de los tiempos de cpu para cada proceso, así poder obtener los tiempos de retorno de cada uno.
        lista_nueva[x].append(acumulador_tiempo_ret)  # Se añade a la «matriz» el tiempo de retorno 'en turno'.
        if acumulador_tiempo_esp - lista_nueva[x][1] <= 0:
            acumulador_tiempo_esp = 0
        else:
            acumulador_tiempo_esp -= lista_nueva[x][1]
        lista_nueva[x].append(acumulador_tiempo_esp)
        acumulador_tiempo_esp = acumulador_tiempo_ret
    for u,v,w,x,y,z in lista_nueva:
        print u,"\t",v,"\t",w,"\t",x,"\t",y,"\t",z
    return procesos_ordenados_x_llegada2

#export PATH='/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games'
incremental = 0.999  # Variable usada para poder llevar un mejor control sobre el ordenamiento en donde los tiempos de cpu se repiten.
def algoritmo_sjf(procesos_ordenados_x_llegada):
    procesos_ordenados_x_llegada = procesos_ordenados_x_llegada
    procesos_ordenados_x_tiempo_de_rafaga = {}  # Inicializo el diccionario
    lista_poxtr = []  # Lista con los tiempos de ráfaga. (poxtr = Procesos ordenados x tiempo de ráfaga)
#    incremental = 0.999
#    for each_process in procesos_ordenados_x_llegada[1:]:
    def function(each_process):
        global incremental
        if each_process[2] not in procesos_ordenados_x_tiempo_de_rafaga:
            lista_poxtr.append(each_process[2])
            procesos_ordenados_x_tiempo_de_rafaga[each_process[2]] = each_process
            #incremental += 0.1
        else:
            lista_poxtr.append(each_process[2]+ incremental)
            procesos_ordenados_x_tiempo_de_rafaga[each_process[2] + incremental] = each_process
            incremental -= 0.001
    for each_process in procesos_ordenados_x_llegada[1:]:
        function(each_process)
    lista_poxtr.sort()
    lista_poxtr.insert(0,procesos_ordenados_x_llegada[0][2])
    function(procesos_ordenados_x_llegada[0])
    lista_poxtr.pop()
    procesos_ordenados_x_tiempo_de_rafaga2 = []
    for x in lista_poxtr:
        procesos_ordenados_x_tiempo_de_rafaga2.append(procesos_ordenados_x_tiempo_de_rafaga[x])

    acomodo(procesos_ordenados_x_tiempo_de_rafaga2)

    acumulador_tiempo_ret = procesos_ordenados_x_tiempo_de_rafaga2[0][1]
    acumulador_tiempo_esp = procesos_ordenados_x_tiempo_de_rafaga2[0][1]
    for x in range(len(procesos_ordenados_x_tiempo_de_rafaga2)):
        acumulador_tiempo_ret += procesos_ordenados_x_tiempo_de_rafaga2[x][2]
        procesos_ordenados_x_tiempo_de_rafaga2[x].append(acumulador_tiempo_ret)
        if acumulador_tiempo_esp - procesos_ordenados_x_tiempo_de_rafaga2[x][1] <=0:
            acumulador_tiempo_esp = 0
        else:
            acumulador_tiempo_esp -= procesos_ordenados_x_tiempo_de_rafaga2[x][1]
        procesos_ordenados_x_tiempo_de_rafaga2[x].append(acumulador_tiempo_esp)
        acumulador_tiempo_esp = acumulador_tiempo_ret
    # Parche ----
    for x in range(len(procesos_ordenados_x_tiempo_de_rafaga2)):
        while len(procesos_ordenados_x_tiempo_de_rafaga2[x]) > 6:
            procesos_ordenados_x_tiempo_de_rafaga2[x].pop()
    # -----------
    print "\nNomP\tLL\tRCpu\tPrior!\tTRet\tTEsp"
    for u,v,w,x,y,z in procesos_ordenados_x_tiempo_de_rafaga2:
        print u,"\t",v,"\t",w,"\t",x,"\t",y,"\t",z

    """for x in lista_poxtr:
        print x," ",procesos_ordenados_x_tiempo_de_rafaga[x]"""
    """np.sort()
    np.insert(0,procesos[0][2])
    print np
    for x in range(len(procesos)):
        for u in np:
            print procesos[x].index(u)"""
def acomodo(lista_procesos):
    # Pequeña función que se encarga de mostrar en pantalla las listas que se pasen como parámetro, añadiendo una tabulaciones para una buena presentación.
    print "NomP\tLL\tRCpu\tPrior!"
    for w,x,y,z in lista_procesos:
        print w,"\t",x,"\t",y,"\t",z

if __name__ == '__main__':
	main()

"""
Notas
Números son repetición
#
startList = [5,1,2,1,3,4,2,5,3,4]
d = {}
[ d.setdefault(x,x) for x in startList if x not in d ] [5, 1, 2, 3, 4]

And for the 'I must do it on one line' freaks, here's the single expression
variant of the above: :^)
[ d.setdefault(x,x) for d in [{}] for x in startList if x not in d ]
-----------------------------------------------------------------------------
"""
