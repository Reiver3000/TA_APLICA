import sys

class Problem(object):
    def __init__(self, initial, goal=None):
        """ Este constructor especifica el estado inicial y posiblemente el estado(s) objetivo(s),
            La subclase puede añadir mas argumentos.
        """
        self.initial = initial
        self.goal = goal

    def actions(self, state):
        """ Retorna las acciones que pueden ser ejecutadas en el estado dado.
            El resultado es tipicamente una lista.
        """
        raise NotImplementedError

    def result(self, state, action):
        """ Retorna el estado que resulta de ejecutar la accion dada en el estado state.
            La accion debe ser alguna de self.actions(state).
        """
        raise NotImplementedError

    def goal_test(self, state):
        """Retorna True si el estado pasado satisface el objetivo."""
        raise NotImplementedError

    def path_cost(self, c, state1, action, state2):
        """ Retorna el costo del camino de state2 viniendo de state1 con
            la accion action, asumiendo un costo c para llegar hasta state1.
            El metodo por defecto cuesta 1 para cada paso en el camino.
        """
        return c + 1

    def value(self, state):
        """ En problemas de optimizacion, cada estado tiene un valor. Algoritmos
            como Hill-climbing intentan maximizar este valor.
        """
        raise NotImplementedError

class Node:

    def __init__(self, state, parent=None, action=None, path_cost=0):
        """Crea un nodo de arbol de busqueda, derivado del nodo parent y accion action"""
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.depth = 0
        if parent:
            self.depth = parent.depth + 1

    def expand(self, problem):
        """Devuelve los nodos alcanzables en un paso a partir de este nodo."""
        lista_expandida=[self.child_node(problem, action)
                for action in problem.actions(self.state)]
        return lista_expandida

    def child_node(self, problem, action):
        next_state = problem.result(self.state, action)
        next_node = Node(next_state, self, action,
                    problem.path_cost(self.path_cost, self.state, action, next_state))
        return next_node

    def solution(self):
        """Retorna la secuencia de acciones para ir de la raiz a este nodo."""
        return [node.action for node in self.path()[1:]]

    def path(self):
        """Retorna una lista de nodos formando un camino de la raiz a este nodo."""
        node, path_back = self, []
        while node:
            path_back.append(node)
            node = node.parent
        return list(reversed(path_back))

    def __str__(self):
        return str(self.state)

def depth_first_tree_search(problem,frontier):
    """Search the deepest nodes in the search tree first.
        Search through the successors of a problem to find a goal.
        The argument frontier should be an empty queue.
        Repeats infinitely in case of loops. [Figure 3.7]"""

    frontier.append(Node(problem.initial))
    nodos_visitados=0
    while frontier:
        node = frontier.pop()
        nodos_visitados+=1
        if problem.goal_test(node.state):
            return node,nodos_visitados,len(node.solution())
        frontier.extend(node.expand(problem))
    return None,nodos_visitados

def graph_search(problem, frontier):

    frontier.append(Node(problem.initial))
    explored = set()
    nodos_visitados=1
    nodos_en_memoria=1
    while frontier:
        node = frontier.pop()
        nodos_visitados+=1
        if problem.goal_test(node.state):
            return node,nodos_visitados,len(frontier)+nodos_visitados
        explored.add(node.state)
        frontier.extend(child for child in node.expand(problem)
                        if( (child.state not in explored) and
                        (child not in frontier)))
    return None,nodos_visitados,len(frontier)+nodos_visitados


def iterative_deeping_search(problem):
    nodos_visitados=0
    for depth in range(sys.maxsize):
        result, nodos =depth_limited_search(problem, depth)
        nodos_visitados+=nodos
        if result != 'cutoff':
            return result,nodos_visitados,len(result.solution())

def depth_limited_search(problem, limit=10):
    result, nodos_visitados= recursive_dls(Node(problem.initial), problem, limit)
    return (result,nodos_visitados)

def recursive_dls(node, problem, limit):
    nodos_visitados=0
    if problem.goal_test(node.state):
        nodos_visitados+=1
        return (node,nodos_visitados)
    elif limit==0:
        nodos_visitados+=1
        return ('cutoff',nodos_visitados)
    else:
        cutoff_occurred=False
        for child in node.expand(problem):
            result,nodos_visitadosh=recursive_dls(child,problem, limit-1)
            nodos_visitados+=nodos_visitadosh

            if result=='cutoff':
                cutoff_occurred=True

            elif result is not None:
                return (result,nodos_visitados)
        return ('cutoff',nodos_visitados) if cutoff_occurred else (None,nodos_visitados)

def interseccion(lista1, lista2):
    intrs1=[value for value in lista1 if value.state in [estado.state for estado in lista2]]
    intrs2=[value for value in lista2 if value.state in [estado.state for estado in lista1]]
    return intrs1,intrs2

def bidirectional_search(problem, frontierA, frontierP):

    frontierA.append(Node(problem.initial))
    frontierP.append(Node(problem.goal))

    nodos_visitadosA=[]
    nodos_visitadosP=[]

    exploredA = set()
    exploredP = set()

    #nodos_visitadosA=1
    nodos_en_memoriaA=1

    #nodos_visitadosP=1
    nodos_en_memoriaP=1

    #nodeP=None
    #nodeA=None

    while frontierA and frontierP:
        """
        if nodeP!=None and nodeA!=None:
            if nodeP.state==nodeA.state:
                return nodeA,nodeP
        """
        intrs1,intrs2=interseccion(frontierA,frontierP)
        if len(intrs1)!=0:
            return intrs1[0], intrs2[0]

        nodeA = frontierA.pop()
        nodos_visitadosA.append(nodeA)

        nodeP = frontierP.pop()
        nodos_visitadosP.append(nodeP)
            
        #nodos_visitadosA+=1
        #nodos_visitadosP+=1

        exploredA.add(nodeA.state)
        #print('+',nodeA)
        exploredP.add(nodeP.state)
        #print('-',nodeP)

        frontierA.extend(   child for child in nodeA.expand(problem)
                            if( (child.state not in exploredA) and (child.state not in (ndo.state for ndo in frontierA)))    )
        frontierP.extend(   child for child in nodeP.expand(problem)
                            if( (child.state not in exploredP) and (child.state not in (ndo.state for ndo in frontierP)))    )



    return None,None

class MapSearchProblem(Problem):
    def __init__(self, initial, goal, mapa):
        """El constructor recibe  el estado inicial, el estado objetivo y un mapa (de clase diccionario)"""
        self.initial = initial
        self.goal = goal
        self.map = mapa

    def actions(self, state):
        """ Retorna las acciones ejecutables desde ciudad state.
            El resultado es una lista de strings tipo 'goCity'.
            Por ejemplo, en el mapa de Romania, las acciones desde Arad serian:
            ['goZerind', 'goTimisoara', 'goSibiu']
        """
        neighbors = []
        acciones = []
        neighbors = self.map[int(state)]
        for acc in range(len(neighbors)):
            acciones.append('go' + str(neighbors[acc][0]))
        return acciones

    def result(self, state, action):
        """ Retorna el estado que resulta de ejecutar la accion dada desde ciudad state.
            La accion debe ser alguna de self.actions(state)
            Por ejemplo, en el mapa de Romania, el resultado de aplicar la accion 'goZerind'
            desde el estado 'Arad' seria 'Zerind'
        """

        newState = action[2:]
        return newState

    def goal_test(self, state):
        """Retorna True si state es self.goal"""
        return (self.goal == state)

    def path_cost(self, c, state1, action, state2):
        """ Retorna el costo del camino de state2 viniendo de state1 con la accion action
            El costo del camino para llegar a state1 es c. El costo de la accion debe ser
            extraido de self.map.
        """

        actionCost = 0
        destStates = self.map[int(state1)]
        for acc in range(len(destStates)):
            if (destStates[acc][0] == state2):
                actionCost = float(destStates[acc][1])
                break
        return c + actionCost

from collections import deque

class FIFOQueue(deque):
    """Una cola First-In-First-Out"""
    def pop(self):
        return self.popleft()
