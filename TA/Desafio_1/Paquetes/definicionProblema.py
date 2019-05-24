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
    
    def __lt__(self, node):
        return self.state < node.state
    
    def __eq__(self, other): 
        "Este metodo se ejecuta cuando se compara nodos. Devuelve True cuando los estados son iguales"
        return isinstance(other, Node) and self.state == other.state
    
    def __repr__(self):
        return "<Node {}>".format(self.state)
    
    def __hash__(self):
        return hash(self.state)

class MapSearchProblem(Problem):
    def __init__(self, initial, goal, mapa, heuristicaAux=None):
        """El constructor recibe  el estado inicial, el estado objetivo y un mapa (de clase diccionario)"""
        self.initial = initial
        self.goal = goal
        self.map = mapa
        #print(heuristicaAux)
        self.heuristica=heuristicaAux

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
        #print(destStates)
        #print(state2)        
        for destino in destStates:
            #print(destino)
            #print(destino[0])
            if destino[0]==int(state2):
                #print("IGUALES")
                actionCost = destino[1]
        
        #print(c+actionCost)
        return c + actionCost
        """
        for acc in range(len(destStates)):
            if (destStates[acc][0] == state2):
                actionCost = float(destStates[acc][1])
                break
        print(c+actionCost)
        return c + actionCost
        """
