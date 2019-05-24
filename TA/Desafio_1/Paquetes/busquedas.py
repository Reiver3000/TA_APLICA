import sys
from Paquetes.definicionProblema import *

#____________________________________________________________________________________________________________________________
from collections import deque

class FIFOQueue(deque):
    """Una cola First-In-First-Out"""
    def pop(self):
        return self.popleft()
#____________________________________________________________________________________________________________________________
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
#____________________________________________________________________________________________________________________________
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
#____________________________________________________________________________________________________________________________

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
#____________________________________________________________________________________________________________________________
def interseccion(lista1, lista2):
    intrs1=[value for value in lista1
            if value.state in [estado.state for estado in lista2]]
    intrs2=[value for value in lista2
            if value.state in [estado.state for estado in lista1]]
    bandera=0
    insta=[]
    instb=[]
    for i in intrs1:
        if bandera==1:
            break
        for j in intrs2:
            if (i.state==j.state):
                #print("encontrado")
                #print(i.state)
                #print(j.state)
                insta=[]
                instb=[]
                insta=[i]
                instb=[j]
                bandera=1
                break
    #print(len(insta))
    #print(len(instb))
    #print("los datos intersectados1")
    #for i in insta:
    #    print(i.state)
    #print("los datos intersectados2")
    #for i in instb:
    #    print(i.state)
    return insta,instb
def bidirectional_search(problem, frontierA, frontierP):

    frontierA.append(Node(problem.initial))
    frontierP.append(Node(problem.goal))
    nodos_visitadosA=[]
    nodos_visitadosP=[]
    exploredA = set()
    exploredP = set()
    nodos_en_memoriaA=1
    nodos_en_memoriaP=1

    lista_exploradosA=[] #esto debe eliminarse-----------------------------
    lista_exploradosP=[] #esto debe eliminarse------------------------------
    listaVisitadosA=[]
    listaVisitadosP=[]
    while frontierA and frontierP:
        
        intrs1,intrs2=interseccion(lista_exploradosA,frontierP)#Si se cruzan en los explorados de A
        intrs3,intrs4=interseccion(frontierA,lista_exploradosP)#si se cruzan en los explorados de P
        intrs5,intrs6=interseccion(frontierA,frontierP)#si se cruzan solo en la frontera
        fronteraA=[]
        for i in frontierA:
            fronteraA.append(i.state)
        fronteraP=[]
        for i in frontierP:
            fronteraP.append(i.state)
        #print("LA FRONTERA DE P",fronteraP)
        #print("LA FRONTERA DE A",fronteraA)

        if len(intrs1)!=0:#primero vemos si sse cruzan en los explorados de A
        #    print("primero")
            return intrs1[0], intrs2[0]
        if len(intrs3)!=0:#Luego vemos si sse cruzan en los explorados de P
        #    print("segundo")
            return intrs3[0], intrs4[0]
        if len(intrs5)!=0:# Al ultimo vemos si se estan cruzando las fronteras
        #    print("tercero")
            return intrs5[0], intrs6[0]
        nodeA = frontierA.pop()
        listaVisitadosA.append(nodeA.state)
        nodos_visitadosA.append(nodeA)
        c=[nodeA]
        lista_exploradosA+=c
        #print("NODOS VISITADOS POR A",listaVisitadosA)
        nodeP = frontierP.pop()
        nodos_visitadosP.append(nodeP)
        listaVisitadosP.append(nodeP.state)
        d=[nodeP]
        lista_exploradosP+=d
        #print("NODOS VISITADOS POR P",listaVisitadosP)

        exploredA.add(nodeA.state)
        exploredP.add(nodeP.state)

        frontierA.extend(   child for child in nodeA.expand(problem)
                            if( (child.state not in exploredA) and (child.state not in (ndo.state for ndo in frontierA)) )    )

        frontierP.extend(   child for child in nodeP.expand(problem)
                            if( (child.state not in exploredP) and (child.state not in (ndo.state for ndo in frontierP)) )    )

    return None,None
#____________________________________________________________________________________________________________________________

import heapq
class FrontierPQ:
    "Una Frontera ordenada por una funcion de costo (Priority Queue)"
    
    def __init__(self, initial, costfn=lambda node: node.path_cost):
        "Inicializa la Frontera con un nodo inicial y una funcion de costo especificada (por defecto es el costo de camino)."
        self.heap   = []
        self.states = {}
        self.costfn = costfn
        self.add(initial)
    
    def add(self, node):
        "Agrega un nodo a la frontera."
        cost = self.costfn(node)
        heapq.heappush(self.heap, (cost, node))
        self.states[node.state] = node
        
    def pop(self):
        "Remueve y retorna el nodo con minimo costo."
        (cost, node) = heapq.heappop(self.heap)
        self.states.pop(node.state, None) # remove state
        return node
    
    def replace(self, node):
        "node reemplaza al nodo de la Fontera que tiene el mismo estado que node."
        if node.state not in self:
            raise ValueError('{} no tiene nada que reemplazar'.format(node.state))
        for (i, (cost, old_node)) in enumerate(self.heap):
            if old_node.state == node.state:
                self.heap[i] = (self.costfn(node), node)
                heapq._siftdown(self.heap, 0, i)
                return

    def __contains__(self, state): return state in self.states
    
    def __len__(self): return len(self.heap)

def best_first_graph_search(problem, f):
    """Busca el objetivo expandiendo el nodo de la frontera con el menor valor de la funcion f. Memoriza estados visitados
    Antes de llamar a este algoritmo hay que especificar La funcion f(node). Si f es node.depth tenemos Busqueda en Amplitud; 
    si f es node.path_cost tenemos Busqueda  de Costo Uniforme. Si f es una heurística tenemos Busqueda Voraz;
    Si f es node.path_cost + heuristica(node) tenemos A* """

    frontier = FrontierPQ( Node(problem.initial), f )  # frontera tipo cola de prioridad ordenada por f
    explored = set()     # memoria de estados visitados
    visited_nodes = []   # almacena nodos visitados durante la busqueda
    while frontier:
        node = frontier.pop()
        visited_nodes.append(node)        
        if problem.goal_test(node.state):
            return node, visited_nodes
        explored.add(node.state)
        for action in problem.actions(node.state):
            child = node.child_node(problem, action)
            if child.state not in explored and child.state not in frontier:
                frontier.add(child)
            elif child.state in frontier:
                incumbent = frontier.states[child.state] 
                if f(child) < f(incumbent):
                    frontier.replace(child)
    return None,visited_nodes

                    
def astar_search(problem, heuristic):
    """ Algoritmo A*, un caso especial de best_first_graph_search con f = path_cost + heuristic  """
    f = lambda node: node.path_cost + heuristic(node, problem)
    return best_first_graph_search(problem, f)

def nullheuristic(node, problem):   
    return 0

def h1(node, problem):
    #print(problem.heuristica)
    hrstca = problem.heuristica
    #print(node.state)
    #print(hrstca)
    #print(hrstca[int(node.state)])
    return hrstca[int(node.state)]
