# -*- coding:utf8 -*-


"""============================================================================
								ENUNCIADO 5
								PRACTICA 2
								
	BEURIER Erwan
	CANAVATE VEGA Fernando
	DE LA ROSA Augustin
	NAPOLI Luca 

	This file contains a kind of main. Launches the simulation of the port.
	
	This file is supposed to be launched via console. Not command line arguments.
	
		
TODO:

============================================================================"""


import PortSimulation
import time

if __name__=="__main__":
	PortSimulation.ISDEBUG = False
	port = PortSimulation.Port(20,10, 60*24)
	
	print "Initialisation done. Simulation starting."
	t = time.clock()
	port.simulate()
	t = time.clock() - t
	print "Simulation done in " + str(t) + " seconds."