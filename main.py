# -*- coding:utf8 -*-


"""============================================================================
								ENUNCIADO 5
								PRACTICA 2
								
	BEURIER Erwan
	CANAVATE VEGA Fernando
	DE LA ROSA Augustin
	NAPOLI Luca 

	This file contains the main executable. Launches the simulation of the port 
	and prints the results.
	
	This file is supposed to be launched via console:
		python main.py [debug] [log] [safe] [--days d] [--hours h] [--mins m]
						[--tugs t] [--wharves w]
	Or: 
		python main.py [debug] [log] [safe] [-d d] [-h h] [-m m] [-t t] [-w w]
		
	(Or any combination of both)
	
	Arguments:
		debug			The string "debug". If present, launches the debug mode of 
						the file. This will print the states during crucial points 
						of the execution and interrupt the execution at each iteration 
						(see PortSimulation.simulate()).
		log 			The string "log". If present, will print the complete state 
						of the port at each iteration.
		safe 			The string "safe". If present, the file will use the safe 
						mode of the Port. It means that the tugs give priority to 
						the oil tankers at the wharves over the ones in the entrance.
		--days d		Adds "d" days to the simulation. Default time is set to one week.
		-d d 			Other version of "--days d".
		--hours h 		Adds "h" hours to the simulation. Default time is set to one week.
		-h h			Other version of "--hours h".
		--mins m 		Adds "m" minutes to the simulation. Default time is set to one week.
		-m m			Other verison of "--mins m".
		--tugs t 		Sets the number of tugs to "t". Default number is 10.
		-t t 			Other version of "--tugs t".
		--wharves w		Sets the number of wharves to "w". Default number is 20.
		-w w			Other version of "--wharves w".
		

============================================================================"""


import PortSimulation
import time
import sys



def readArgs(argv):
	"""
	Function that reads the command line arguments and returns what it reads, 
	in terms of times, number of tugs and number of wharves.
	
	Arguments: 
		argv		Supposed to be sys.argv.
	"""
	
	if "debug" in argv:
		PortSimulation.ISDEBUG = True
		argv.remove("debug")
	if "safe" in argv:
		PortSimulation.SAFEPORT = True 
		argv.remove("safe")
	if "log" in argv:
		PortSimulation.LOGPORT = True
		argv.remove("log")
	
	wharves = 20
	tugs = 10
	time = 0
	timeChanged = False
	
	for i in xrange(len(argv)):
		if argv[i] == "--hours" or argv[i] == "-h":
			i += 1
			time += int(argv[i]) * 60
			timeChanged = True 
		elif argv[i] == "--mins" or argv[i] == "-m":
			i += 1
			time += int(sys.argv[i])
			timeChanged = True 
		elif argv[i] == "--days" or argv[i] == "-d":
			i += 1
			time += int(sys.argv[i])*60*24
			timeChanged = True 
		elif argv[i] == "--tugs" or argv[i] == "-t":
			i += 1
			tugs = int(sys.argv[i])
		elif argv[i] == "--wharves" or argv[i] == "-w":
			i += 1
			wharves = int(sys.argv[i])
	
	if not timeChanged:
		time = 24*60*7 #Default value, just in case.
	
	return wharves, tugs, time
			



"""============================================================================
	M 	  M       A 	  II	NN     N 
	MM	 MM      A A	  II   	N N    N
	M M	M M     A   A	  II   	N  N   N
	M  M  M     AAAAA	  II   	N   N  N
	M	  M    A     A	  II	N    N N
	M 	  M	  A       A   II	N     NN
============================================================================"""

if __name__=="__main__":
	try:
		wharves, tugs, tiempo = readArgs(sys.argv)
	except IndexError:
		print "Error: something went wrong with the arguments."
	
	#port = PortSimulation.Port(20, 10, 60*24*7)
	port = PortSimulation.Port(wharves, tugs, tiempo)
	#
	
	print "Initialisation done. Simulation starting."
	t = time.clock()
	port.simulate()
	t = time.clock() - t
	print "Simulation done in " + str(t) + " seconds."
	port.printResults()
	
	
	
	