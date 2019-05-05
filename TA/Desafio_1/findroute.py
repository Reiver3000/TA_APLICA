import sys
import time
import numpy as np
from random import shuffle, random, sample, randint
from copy import deepcopy
from math import exp

class Problem(object):

    """

    The abstract class for a formal problem. You should subclass
    this and implement the methods actions and result, and possibly
    __init__, goal_test, and path_cost. Then you will create instances
    of your subclass and solve them with the various search functions.
    """

    def __init__(self, initial, goal=None):
        """
        The constructor specifies the initial state, and possibly a goal
        state, if there is a unique goal. Your subclass's constructor can add
        other arguments.
        """
        self.initial = initial
        self.goal = goal

    def actions(self, state):
        """
        Return the actions that can be executed in the given
        state. The result would typically be a list, but if there are
        many actions, consider yielding them one at a time in an
        iterator, rather than building them all at once.
        """
        raise NotImplementedError

    def result(self, state, action):
        """
        Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state).
        """
        raise NotImplementedError

    def goal_test(self, state):
        """
        Return True if the state is a goal. The default method compares the
        state to self.goal or checks for state in self.goal if it is a
        list, as specified in the constructor. Override this method if
        checking against a single self.goal is not enough.
        """
        if isinstance(self.goal, list):
            return is_in(state, self.goal)
        else:
            return state == self.goal

    def path_cost(self, c, state1, action, state2):
        """
        Return the cost of a solution path that arrives at state2 from
        state1 via action, assuming cost c to get up to state1. If the problem
        is such that the path doesn't matter, this function will only look at
        state2.  If the path does matter, it will consider c and maybe state1
        and action. The default method costs 1 for every step in the path.
        """
        return c + 1

    def value(self, state):
        """
        For optimization problems, each state has a value.  Hill-climbing
        and related algorithms try to maximize this value.
        """
        raise NotImplementedError
"""
````
``````````````
________________________________________________________________________________
"""

def readCommand( argv ):
	"""
	Procesa los argumentos de la linea de comandos
	"""
	from optparse import OptionParser
	usageStr = """
	USAGE:      python findroute.py <options>
	EXAMPLES:   python findroute.py -e edges_pitts.txt –s 275754986 -g 105012740 –m astar -h heuristics_pitts.txt
                python findroute.py -e --help

	"""

	parser = OptionParser(usageStr)
	parser.add_option('-e', '--calles',    dest='calles',  help=default('El nombre del archivo con las calles'),   default='edges_pitts.txt')
	parser.add_option('-s', '--nodoI',     dest='nodoI',   help=default('nodeID inicial'),                         default='104878620')
	parser.add_option('-g', '--nodoF',     dest='nodoF',   help=default('nodeID final'),                           default='105012740')
    parser.add_option('-m', '--busqueda',  dest='busqueda', help=default('Metodo de busqueda e.g: bfs, dfs, etc.'),default='bfs')
	parser.add_option('-h', '--heuristica',dest='heuristica',help=default('heuristica para Astar search'),         default=None)

	options, otherjunk = parser.parse_args(argv)

	if len(otherjunk) != 0:
		raise Exception('Command line input not understood: ' + str(otherjunk))

	fd = open(options.calles,"r")    # lee el nombre de las calles
	lineas = fd.readlines()
    lista=[]
	for linea in lineas:
	    lista.append(linea.split())

	mapa = dict()
	for sublista in lista:
		if sublista[0] in mapa: mapa[sublista[0]].append((sublista[1],sublista[2]))
	    else mapa[sublista[0]]=[(sublista[1],sublista[2])]

	    if sublista[1] in mapa: mapa[sublista[1]].append((sublista[0],sublista[2]))
	    else mapa[sublista[1]]=[(sublista[0],sublista[2
	print(mapa)

    if options.heuristica!=None:
        fd1=open(options.heuristica,"r")
        lineas1= fd.readlines()
        lista1=[]
        for linea1 in lineas1:
            lista1.append(linea1.split())


    args = dict()
	args['mapa'] = mapa  # puzzle es un vector con todas las filas del puzzle concatenadas (vacios tiene valor 0)
	args['nodoI'] = options.nodoI
	args['nodoF'] =  options.nodoF
    args['busqueda'] = options.busqueda
    if options.heuristica!=None:
        args['heuristica'] = lista1
    else:
        args['heuristica'] = options.heuristica

	return args

if __name__=="__main__":
	"""
	The main function called when findroute.py is run from the command line:
	> python sudokusolver.py

	See the usage string for more details.

	> python findroute.py --help
    """
	args = readCommand( sys.argv[1:] ) # Get the arguments from the command line input
	solvers = {'sa': sa_solver,	'ga': ga_solver }  # Dictionary of available solvers

	solvers[args['solver']]( args['puzzle'], args['solverParams'] )  # Call the solver method passing the string of

"""
viste endgame otra vez? (╯°□°）╯︵ ┻━┻

no no solo sali un toque xdd

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
