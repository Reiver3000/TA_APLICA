import sys
"""
import time
import numpy as np
from random import shuffle, random, sample, randint
from copy import deepcopy
from math import exp
"""
#____________________________________________________________________________________________________________________________

from Paquetes.linea_de_comando import readCommand
from Paquetes.busquedas import *

if __name__=="__main__":
	"""
	The main function called when findroute.py is run from the command line:
	> python sudokusolver.py

	See the usage string for more details.

	> python findroute.py --help
    """

	args = readCommand( sys.argv[1:] )


	"""Instancia el problema de busqueda con nodo inicial 'nodoI' y nodo objetivo 'nodoF'"""
	map_problem = MapSearchProblem(args['nodoI'], args['nodoF'], args['mapa'], args['heuristica'])

	if(args['busqueda']=='bfs'):
		"""Ejecutar busqueda en Amplitud (BFS) """
		node_solucionBFS,nodos_visitados,nodos_en_memoria = graph_search(map_problem, FIFOQueue())
		if node_solucionBFS!=None:
			print( 'Ruta encontrada: {}'.format(node_solucionBFS.solution()))
			print( 'Costo de la ruta encontrada {}'.format(node_solucionBFS.path_cost))
			print( 'Numero de nodos en la ruta encontrada {}'.format(len(node_solucionBFS.solution())))
			print( 'Numero de nodos visitados: {}'.format(nodos_visitados) )
			print( 'Numero de nodos en memoria: {}'.format(nodos_en_memoria))
		else:
			print("No hay solución BFS")

	if(args['busqueda']=='dfs'):
		"""Ejecutar busqueda en Profundidad (DFS) """
		node_solucionDFS,nodos_visitados,nodos_en_memoria = graph_search(map_problem, [])
		if node_solucionDFS!=None:
			print( 'Ruta encontrada: {}'.format(node_solucionDFS.solution()) )
			print( 'Costo de la ruta encontrada {}'.format(node_solucionDFS.path_cost))
			print( 'Numero de nodos en la ruta encontrada {}'.format(len(node_solucionDFS.solution())))
			print( 'Numero de nodos visitados: {}'.format(nodos_visitados) )
			print( 'Numero de nodos en memoria: {}'.format(nodos_en_memoria))
		else:
			print("No hay solución DFS")

	if(args['busqueda']=='ids'):
		"""Ejecutar busqueda iterativa en Profundidad (IDS) """
		node_solucionIDS,nodos_visitados, nodos_en_memoria = iterative_deeping_search(map_problem)
		if node_solucionIDS!=None:
			print( 'Ruta encontrada: {}'.format(node_solucionIDS.solution()) )
			print( 'Costo de la ruta encontrada {}'.format(node_solucionIDS.path_cost))
			print( 'Numero de nodos en la ruta encontrada {}'.format(len(node_solucionIDS.solution())))
			print( 'Nro de nodos visitados: {}'.format(nodos_visitados) )
			print( 'Nro de nodos en memoria: {}'.format(nodos_en_memoria))
		else:
			print("No hay solución IDS")

	if(args['busqueda']=='bis'):
		"""Ejecutar busqueda Bidireccional (BIS) """
		node_solucionBIS1, node_solucionBIS2= bidirectional_search(map_problem,FIFOQueue(),[])
		nodos_visitados=[] #Falta implementar=================================================================
		nodos_en_memoria=[] #Falta implementar================================================================
		if node_solucionBIS1!=None:

			solucion1=node_solucionBIS1.solution()
			solucion2=node_solucionBIS2.solution()

			solv=[]
			cant=len(solucion2)
			for i in range(cant):
				c1=solucion2.pop()
				solv.append(c1)
			
			respuesta= solucion1+solv
			solucion3=[]
			for i in respuesta:
				if i not in solucion3:
					solucion3.append(i)
			
			print( 'Ruta encontrada: {}'.format(solucion3) )
			print( 'Costo de la ruta encontrada {}'.format(node_solucionBIS1.path_cost+node_solucionBIS2.path_cost))
			print( 'Numero de nodos en la ruta encontrada {}'.format(len(solucion3)))
			print( 'Numero de nodos visitados: {}'.format(nodos_visitados) )
			print( 'Numero de nodos en memoria: {}'.format(nodos_en_memoria))
		else:
			print("No hay solución BIS")

	if(args['busqueda']=='astar'):
		"""Ejecutar busqueda A* """

		node_solucionASTAR, nodos_visitados=astar_search(map_problem,h1)
		nodos_en_memoria=[] #Falta implementar================================================================
		if node_solucionASTAR!=None:
			print( 'Ruta encontrada: {}'.format(node_solucionASTAR.solution()) )
			print( 'Costo de la ruta encontrada: {}'.format(node_solucionASTAR.path_cost))
			print( 'Numero de nodos en la ruta encontrada: {}'.format(len(node_solucionASTAR.solution())))
			print( 'Nro de nodos visitados: {}'.format(nodos_visitados) )
			print( 'Nro de nodos en memoria: {}'.format(nodos_en_memoria))
		else:
			print("No hay solucion Astar")
#____________________________________________________________________________________________________________________________
"""
(╯°□°）╯︵ ┻━┻

DATOS DE PRUEBA

1 3 5.0
1 4 4.0
1 8 2.0`
2 5 5.0
2 7 9.0
2 8 1.0
2 10 7.0
3 6 6.0
4 5 7.0
5 6 7.0
5 9 8.0
6 9 1.0
7 10 3.0
7 8 5.0
9 10 2.0
"""
