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
from Paquetes.busquedas import graph_search,MapSearchProblem,FIFOQueue

if __name__=="__main__":
	"""
	The main function called when findroute.py is run from the command line:
	> python sudokusolver.py

	See the usage string for more details.

	> python findroute.py --help
    """
	args = readCommand( sys.argv[1:] )

	"""
	print(args['nodoI'])
	print(args['nodoF'])
	print(args['busqueda'])
	print(args['mapa'])
	"""

	"""Instancia el problema de busqueda con nodo inicial 'nodoI' y nodo objetivo 'nodoF' """
	romania_problem = MapSearchProblem(args['nodoI'], args['nodoF'], args['mapa'])

	"""Ejecutar busqueda en Amplitud (BFS) """
	node_solucionBFS = graph_search(romania_problem, FIFOQueue())
	print( 'Solucion del Problema de Busqueda en mapa de Romania con BFS: {}'.format(node_solucionBFS.solution()) )

	"""Ejecutar busqueda en Profundidad (DFS) """
	node_solucionDFS = graph_search(romania_problem, [])  # una lista [] es una pila en Python
	print( 'Solucion del Problema de Busqueda en mapa de Romania con DFS: {}'.format(node_solucionDFS.solution()) )


	"""solvers = {'sa': sa_solver,	'ga': ga_solver }  # Dictionary of available solvers

	solvers[args['solver']]( args['puzzle'], args['solverParams'] )  # Call the solver method passing the string of"""


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
