#!/usr/bin/env python
#-*-coding:utf-8-*-

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

random.seed()

def main():
	cantidad_de_procesos = random.randint(1, 50)
	
	# Inicializar la lista de procesos
	procesos = []
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
	print "\n",nuevos_tiempos_de_llegada[:cantidad_de_procesos]
	 
#export PATH='/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games'

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