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
	parser.add_option('-e', '--calles', dest='calles', help= default('El nombre del archivo con las calles'), default='Archivos/edges_pitts.txt')
	parser.add_option('-s', '--nodoI', dest='nodoI', help= default('nodeID inicial'), default='104878620')
	parser.add_option('-g', '--nodoF', dest='nodoF', help= default('nodeID final'), default='105012740')
	parser.add_option('-m', '--busqueda', dest='busqueda', help= default('Metodo de busqueda e.g: bfs, dfs, etc.'), default='bfs')
	parser.add_option('-h', '--heuristica', dest='heuristica', help= default('heuristica para Astar search'), default=None)

	options, otherjunk = parser.parse_args(argv)

	if len(otherjunk) != 0:
		raise Exception('Command line input not understood: ' + str(otherjunk))

	e_pits_txt = open(options.calles,"r")    # lee el nombre de las calles
	lineas = e_pits_txt.readlines()
	lista=[]
	for linea in lineas:
	    lista.append(linea.split())

	mapa = dict()
	for sublista in lista:
		if sublista[0] in mapa:
			mapa[sublista[0]].append((sublista[1],sublista[2]))
		else:
			mapa[sublista[0]]=[(sublista[1],sublista[2])]
		
		if sublista[1] in mapa:
			mapa[sublista[1]].append((sublista[0],sublista[2]))
		else:
			mapa[sublista[1]]=[(sublista[0],sublista[2])]
			
		print(mapa)
		
	if options.heuristica!=None:
		h_pitts_txt=open(options.heuristica,"r")
		lineas= h_pitts_txt.readlines()
		h_pitts=[]
		for linea in lineas:
			h_pitts.append(linea.split())
			
	args = dict()
	args['mapa'] = mapa  # puzzle es un vector con todas las filas del puzzle concatenadas (vacios tiene valor 0)
	args['nodoI'] = options.nodoI
	args['nodoF'] =  options.nodoF
	args['busqueda'] = options.busqueda
    
	if options.heuristica!=None:
		args['heuristica'] = h_pitts
	else:
		args['heuristica'] = options.heuristica

	return args