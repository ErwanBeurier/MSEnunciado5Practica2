# -*- coding:utf8 -*-


"""============================================================================
								ENUNCIADO 5
								PRACTICA 2
								
	BEURIER Erwan
	CANAVATE VEGA Fernando
	DE LA ROSA Augustin
	NAPOLI Luca 

	This file contains the implementation of the class Port.
	Useful methods:
		simulate()
	(The rest is supposed to be private, even if Python doesn't know about 
	encapsulation)
	
	This file is not supposed to be launched via console.
	
	
	Vocabulary (because the code is in English but the wording is in Spanish):
		tug 		= remolcador
		oil tanker	= petrolero
		wharf 		= muelle
	
	
TODO:
	routineArrivalOilTankerWharf : risk of blocked situation.
	add the attributes that enable to answer the questions LOL
============================================================================"""



import random
from scipy.stats import t as tStudent
from scipy.stats import norm
import ListEvents
import OilTanker


ISDEBUG = True 

class Port:
	"""
	The class managing the port.
	
	Attributes:
		maxWharves				Total number of wharves in the port.
		maxTugs					Total number of tugs in the port.
		oilTankersEntrance		Queue at the entrance of the port.
		oilTankersWharves	 	List of OilTankers that are currently unloading.
		oilTankersWharvesDone	List of OilTankers that have finished unloading.
		freeTugs				Number of free tugs in the port.
		time					The clock in the port (in minutes). Updates at 
								each iteration of the method Port.simulate().
		maxTime					The time that the simulation is supposed to last 
								(in minutes).
		listEvents				A register that stores events, their time of 
								occurrence, and the concerned oil tanker, if any.
		muEmpty					The mean of the time took by the tugs to reach 
								their destination when empty.
		sigEmpty 				The standard deviation of the time took by the 
								tugs to reach their destination when empty.
		muFull 					The mean of the time took by the tugs to reach 
								their destination when carrying an oil tanker.
		sigFull 				The standard deviation of the time took by the 
								tugs to reach their destination when carrying 
								an oil tanker.
		tankerCountDone			Counts the number of tankers done.
		tankerCountInside		Counts the number of tankers inside.
		tankerCountWaiting		Counts the number of tankers waiting.
		tankerCountTotalGenerated	Counts the number of generated tankers. 
								Mandatory to identify tankers (a tanker has an 
								id).
		cumulTimeTankersDone	Counts the time took by tankers inside the port.

	"""
	def __init__(self, maxWharves, maxTugs, timeSimulation, muEmpty = 2, sigEmpty = 1, muFull = 10, sigFull = 3):
		"""
		Constructor. 
		
		Arguments:
			maxWharves			The maximum number of wharves in the port.
			maxTugs				The maximum number of tugs in the port.
			timeSimulation		The duration of the simulation.
			muEmpty				The mean of the time took by the tugs to reach 
								their destination when empty.
			sigEmpty			The standard deviation of the time took by the 
								tugs to reach their destination when empty.
			muFull				The mean of the time took by the tugs to reach 
								their destination when carrying an oil tanker.
			sigFull				The standard deviation of the time took by the 
								tugs to reach their destination when carrying 
								an oil tanker.
		"""
		self.debugDebug("Initialization starting.")
		self.maxWharves = maxWharves
		self.maxTugs = maxTugs
		self.oilTankersEntrance = [] # No limit on size.
		self.oilTankersWharves = [] # Needs to be of size <= maxWharves
		self.oilTankersWharvesDone = [] # The indices in oilTankerWharves that have finished unloading.
		self.freeTugs = maxTugs # size <= maxTugs
		self.time = 0.0
		self.maxTime = timeSimulation
		self.listEvents = ListEvents.ListEvents()
		self.muEmpty = muEmpty
		self.sigEmpty = sigEmpty
		self.muFull = muFull
		self.sigFull = sigFull
		self.tankerCountDone = 0
		self.tankerCountInside = 0
		self.tankerCountWaiting = 0
		self.tankerCountTotalGenerated = 0 # Increments 
		self.cumulTimeTankersDone = 0.0
		self.debugDebug("End of initialization.")
	
	
	
	def simulate(self):
		"""
		Launches the simulation. It generates a first oil tanker then launches 
		a loop. The loop iterates on time. 
		At each iteration, we get the type of next event, the time at which it 
		occurs, and potentially an oil tanker if the event concerns an oil tanker.
		Then it checks which event is the next and uses the corresponding routine.
		The loop stops after some time, given at the construction of the instance.
		"""
		self.debugDebug("Simulation starting.")
		self.generateOilTanker()		
		event = ""
		oilTanker = None 
		
		while self.time < self.maxTime:
			event, self.time, oilTanker = self.listEvents.getNextEvent()
			self.debugDebug("Step : " + event + " after time : "+ str(self.time) + "Oil Tanker : " + str(oilTanker))
			
			if event == "ArrivalOilTankerEntrance":
				self.routineArrivalOilTankerEntrance(oilTanker)
			elif event == "ArrivalTugEntrance":
				self.routineArrivalTugEntrance()
			elif event == "ArrivalOilTankerWharf":
				self.routineArrivalOilTankerWharf(oilTanker)
			elif event == "UnloadingDone":
				self.routineUnloadingDone(oilTanker)
			elif event == "ArrivalTugWharf":
				self.routineArrivalTugWharf()
			elif event == "ExitOilTanker":
				self.routineExitOilTanker(oilTanker)
			elif event == "TugAvailable":
				self.routineTugAvailable()
				
			self.debugDebug("Event to remove : " + event)
			self.listEvents.removeLastEvent(event)
			# print self.listEvents
		
		
		
	def generateOilTanker(self):
		"""
		Used to generate an OilTanker. Simulates an exponential variate of 
		parameter Port.lambdat, adds the OilTanker to the list of events.
		"""
		self.tankerCountTotalGenerated += 1
		t = random.expovariate(self.lambdat())
		#self.oilTankersEntrance.append(OilTanker(t, self.tankerCountTotalGenerated))
		self.listEvents.addEvent("ArrivalOilTankerEntrance", self.time + t, OilTanker.OilTanker(self.time + t, self.tankerCountTotalGenerated))
	
	
	
	def lambdat():
		"""
		Generates the lambda depending on the time "t".
		"""
		t = self.time % 24.0
		lt = 0
		if 0.0 <= t and t < 5.0:
			lt = 2.0/5.0*t + 5.0
		elif 5.0 <= t and t < 9.0:
			lt = -1.0/4.0*t + 33.0/4
		elif 9.0 <= t and t < 15.0:
			lt = 1.0/2.0*t + 3.0/2.0
		elif 15.0 <= t and t < 17.0:
			lt = -3.0/2.0*t + 63.0/2.0
		else:
			lt = -1.0/7.0*t + 59.0/7.0
		return lt
	
	
	
	def routineArrivalOilTankerEntrance(self, oilTanker):
		"""
		Routine supposed to be triggered when "oilTanker" arrives at the entrance
		of the port.
		When "oilTanker" arrives at the entrance:
			- increment the number of waiting tankers + add it to the list 
			self.oilTankersEntrance (which is the queue in the entrance of the 
			port)
			- generate another arrival of another tanker.
			- if a tug is free, we ask it to come take the oilTanker (i.e. add 
			the event "ArrivalTugEntrance" after a time Normal(self.muEmpty, self.sigEmpty))
			
		Arguments:
			oilTanker		The arriving oil tanker.
		"""
		self.tankerCountWaiting += 1
		self.generateOilTanker()
		self.oilTankersEntrance.append(oilTanker)
		
		if self.freeTugs > 0:
			self.freeTugs -= 1
			t = random.normalvariate(self.muEmpty, self.sigEmpty)
			self.listEvents.addEvent("ArrivalTugEntrance", self.time + t)
			
			
	
	def routineArrivalTugEntrance(self):
		"""
		Routine supposed to be triggered when a tug arrives at the entrance of 
		the port to take an oil tanker.
		The tug takes the first oil tanker and leads it to a wharf. It adds an 
		event "ArrivalOilTankerWharf" to the list.
		"""
		t = random.normalvariate(self.muFull, self.sigFull)
		ot = self.oilTankersEntrance[0]
		self.oilTankersEntrance.remove(ot)
		self.listEvents.addEvent("ArrivalOilTankerWharf", self.time + t, ot)
		self.tankerCountWaiting -= 1
		self.tankerCountInside += 1

	
	def routineArrivalOilTankerWharf(self, oilTanker):
		"""
		Routine supposed to be triggered when "oilTanker" arrives at the wharf.
		The oilTanker is preparing to unload its content and it frees the tug.
		Adds the events "TugAvailable" and "UnloadingDone" to the list.
		
		Arguments:
			oilTanker		The oil tanker that arrives to the wharf.

		OJO
		There can be a blocked situation here!
		If: the wharves are full 
			+ the oilTankers in the wharves need a tug to exit the wharves 
			+ the tugs are carrying an oil tanker to the wharves
		
		"""
		if len(self.oilTankersWharves) + len(self.oilTankersWharvesDone) < 20: 
			# It means that a wharf is free to deal with the oilTanker.
			self.listEvents.addEvent("TugAvailable", self.time)
			t = tStudent.rvs(3)
			self.listEvents.addEvent("UnloadingDone", self.time + t, oilTanker)
			self.oilTankersWharves.append(oilTanker)
		else:
			print "Risk of blocked situation. I don't kow how to handle it."
			raw_input()
	
	
	
	def routineUnloadingDone(self, oilTanker):
		"""
		Routine supposed to be triggered when "oilTanker" is done unloading at 
		a wharf.
		Moves "oilTanker" from self.oilTankersWharves to self.oilTankersWharvesDone
		and calls for a tug is one is free (i.e. it adds an event "ArrivalTugWharf" 
		if a tug is avaiblable.)
		
		Arguments:
			oilTanker 		The oil tanker whose unloading is done.
		"""
		self.oilTankersWharves.remove(oilTanker)
		self.oilTankersWharvesDone.append(oilTanker)
		
		if self.freeTugs > 0:
			self.freeTugs -= 1
			t = random.normalvariate(self.muEmpty, self.sigEmpty)
			self.listEvents.addEvent("ArrivalTugWharf", self.time + t)

			
			
	def routineArrivalTugWharf(self):
		"""
		Routine supposed to be triggered when a tug arrives at a wharf to take 
		care of an oil tanker.
		Starts the evacuation of the oil tanker.
		Adds "ExitOilTanker" to the list of events.
		"""
		t = random.normalvariate(self.muFull, self.sigFull)
		ot = self.oilTankersWharvesDone[0]
		self.oilTankerWharvesDone = self.oilTankersWharvesDone[1:]
		self.listEvents.addEvent("ExitOilTanker", self.time + t, ot)
		
	
	
	def routineExitOilTanker(self, oilTanker):
		"""
		Routine supposed to be triggered when "oilTanker" exits the port.
		Here are supposed to occur the whole steps of calculations.
		Then the tug is available (adds an event "TugAvailable" to the list).
		
		Arguments:
			oilTanker		The oil tanker that leaves the port.
		"""
		self.cumulTimeTankersDone = oilTanker.getTotalTime()
		self.tankerCountInside -= 1
		self.tankerCountDone += 1
		self.listEvents.addEvent("TugAvailable", self.time)
		
	
	
	def routineTugAvailable(self):
		"""
		Routine supposed to be triggered when a tug becomes available.
		If a tug becomes available while there are some oil tankers waiting in 
		the entrance, the tug will take care of them (i.e. adds an event 
		"ArrivalTugEntrance" to the list).
		If a tug becomes available while the queue at the entrance is empty, 
		and an oil tanker is done at the wharves, the tug will go to the wharves 
		(i.e. adds an event "ArrivalTugWharf" to the list).
		Otherwise, the tug becomes available for further use.
		"""
		if len(self.oilTankersEntrance) > 0:
			t = random.normalvariate(self.muEmpty, self.sigEmpty)
			self.listEvents.addEvent("ArrivalTugEntrance", self.time + t)
		elif len(self.oilTankersWharvesDone) > 0:
			t = random.normalvariate(self.muEmpty, self.sigEmpty)
			self.listEvents.addEvent("ArrivalTugWharf", self.time + t)
		elif self.freeTugs < self.maxTugs: # Should not occur, but well...
			self.freeTugs += 1
		
		
		
	def debugDebug(self, s):
		"""
		A classical debug/pause method.
		
		Arguments:
			s 			The text to print before the pause.
		"""
		if ISDEBUG:
			print s
			raw_input()

			
			
			
			
		
		
		
		
		
		