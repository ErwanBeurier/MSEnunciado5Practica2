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
import sys

if __name__=="__main__":
	PortSimulation.ISDEBUG = ("debug" in sys.argv)
	PortSimulation.SAFEPORT = ("safe" in sys.argv)
	PortSimulation.LOGPORT = ("log" in sys.argv)
	
	
	#port = PortSimulation.Port(20, 10, 60*24*7)
	port = PortSimulation.Port(25, 1000, 60*24*7)
	#
	
	print "Initialisation done. Simulation starting."
	t = time.clock()
	port.simulate()
	t = time.clock() - t
	print "Simulation done in " + str(t) + " seconds."
	port.printResults()
	
	
	
	