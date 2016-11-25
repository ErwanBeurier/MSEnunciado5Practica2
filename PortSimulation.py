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
		printResults()
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
from scipy.stats import chi2
import ListEvents
import OilTanker


ISDEBUG = True 
SAFEPORT = False
LOGPORT = True

def minutesToTime(minutes):
	hours = int(minutes/60)
	minutes = int(minutes - hours * 60)
	days = int(hours/24)
	hours = hours - days*24
	return str(days) + "d" + str(hours) + "h" + str(minutes) + "m"


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
		previousTime			The time of the last event. Useful to compute 
								the means.
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
		meanNumOilTankersEntrance	Mean number of oil tankers in the entrance. 
									Updates at every iteration of simulate().
		maxNumOilTankersEntrance	Max number of oil tankers in the entrance. 
									Updates at every iteration of simulate().
		meanNumOilTankersInside		Mean number of oil tankers inside the port. 
									Updates at every iteration of simulate().
		maxNumOilTankersInside		Max number of oil tankers inside the port. 
									Updates at every iteration of simulate().
		meanTimeOilTankerInside		Mean time spent by oil tankers inside the 
									port. Updates at every iteration of simulate().
		maxTimeOilTankerInside		Max time spent by oil tankers inside the 
									port. Updates every time an oil tanker leaves 
									the port.
		meanTimeOilTankersUnloading		Mean time spent by oil tankers to unload. 
										Updates at every iteration of simulate().
		maxTimeOilTankersUnloading		Max time spent by oil tankers to unload. 
										Updates at every iteration of simulate().
		meanNumOilTankersWharves	Mean number of oil tankers at the wharves. 
									Updates at every iteration of simulate().
		maxNumOilTankersWharves 	Max number of oil tankers at the wharves. 
									Updates at every iteration of simulate().
	"""
	def __init__(self, maxWharves, maxTugs, timeSimulation, muEmpty = 2, sigEmpty = 1, muFull = 10, sigFull = 3):
		"""
		Constructor. 
		
		Arguments:
			maxWharves			The maximum number of wharves in the port.
			maxTugs				The maximum number of tugs in the port.
			timeSimulation		The duration of the simulation.
			muEmpty				The mean of the time took by the tugs to reach 
								their destination when empty. In minutes.
			sigEmpty			The standard deviation of the time took by the 
								tugs to reach their destination when empty. In 
								minutes.
			muFull				The mean of the time took by the tugs to reach 
								their destination when carrying an oil tanker. 
								In minutes.
			sigFull				The standard deviation of the time took by the 
								tugs to reach their destination when carrying 
								an oil tanker. In minutes.
		"""
		self.debugDebug("Initialization starting.")
		self.maxWharves = maxWharves
		self.maxTugs = maxTugs
		self.oilTankersEntrance = [] # No limit on size.
		self.oilTankersWharves = [] # Needs to be of size <= maxWharves
		self.oilTankersWharvesDone = [] # The indices in oilTankerWharves that have finished unloading.
		self.freeTugs = maxTugs # size <= maxTugs
		self.time = 0.0
		self.previousTime = 0.0
		self.maxTime = timeSimulation
		self.listEvents = ListEvents.ListEvents()
		self.muEmpty = muEmpty
		self.sigEmpty = sigEmpty
		self.muFull = muFull
		self.sigFull = sigFull
		self.tankerCountDone = 0
		self.tankerCountInside = 0 # Inside = between the moment they leave the entrance queue and the moment they get out of the port.
		self.tankerCountWaiting = 0
		self.tankerCountTotalGenerated = 0 # Increments each time a tanker is generated. 
		self.cumulTimeTankersDone = 0.0
		self.meanNumOilTankersEntrance = 0.0
		self.maxNumOilTankersEntrance = 0.0
		self.meanNumOilTankersInside = 0.0
		self.maxNumOilTankersInside = 0.0
		self.meanTimeOilTankerInside = 0.0 # 
		self.maxTimeOilTankerInside = 0.0
		self.meanTimeOilTankersUnloading = 0.0 # Unloading = between the moment they leave the entrance and the moment they finish unloading.
		self.maxTimeOilTankersUnloading = 0.0
		self.meanNumOilTankersWharves = 0.0 # The mean number of boats at the wharves.
		self.maxNumOilTankersWharves = 0.0
		self.numTimesBlocked = 0
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
		stopThat = False

		while self.time < self.maxTime:
			self.previousTime = self.time
			event, self.time, oilTanker = self.listEvents.getNextEvent()
			self.debugDebug("Step : " + event + " after time : "+ str(self.time) + "Oil Tanker : " + str(oilTanker))
			self.updateTimes()
			
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
				if SAFEPORT:
					self.routineTugAvailableSafe()
				else:
					self.routineTugAvailable()
			
			oilTanker = None
			self.debugDebug("Event to remove : " + event)
			self.listEvents.removeLastEvent(event)
			
			if LOGPORT and not stopThat:
				self.printState()
				stopThat = (raw_input() != "")
			if self.detectBlockedSituation():
				self.numTimesBlocked += 1
		
		self.lastUpdateTimes()
		
		
	def generateOilTanker(self):
		"""
		Used to generate an OilTanker. Simulates an exponential variate of 
		parameter Port.lambdat, adds the OilTanker to the list of events.
		"""
		self.tankerCountTotalGenerated += 1
		lt = self.lambdat()
		t = 60*random.expovariate(lt)
		self.debugDebug(t)
		#self.oilTankersEntrance.append(OilTanker(t, self.tankerCountTotalGenerated))
		ot = OilTanker.OilTanker(self.time + t, self.tankerCountTotalGenerated)
		self.listEvents.addEvent("ArrivalOilTankerEntrance", self.time + t, ot)
	
	
	
	def lambdat(self):
		"""
		Generates the lambda depending on the time "self.time".
		"""
		t = (self.time / 60.0) % 24.0
		lt = 0
		if 0.0 <= t and t < 5.0:
			lt = 2.0*t/5.0 + 5.0
		elif 5.0 <= t and t < 9.0:
			lt = -1.0*t/4.0 + 33.0/4
		elif 9.0 <= t and t < 15.0:
			lt = 1.0*t/2.0 + 3.0/2.0
		elif 15.0 <= t and t < 17.0:
			lt = -3.0*t/2.0 + 63.0/2.0
		else:
			lt = -1.0*t/7.0 + 59.0/7.0
		self.debugDebug(str(t) + " + lambda: " + str(lt))

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
		ot = self.oilTankersEntrance.pop(0)
		#self.oilTankersEntrance.remove(ot)
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
		if len(self.oilTankersWharves) + len(self.oilTankersWharvesDone) < self.maxWharves: 
			# It means that a wharf is free to deal with the oilTanker.
			self.listEvents.addEvent("TugAvailable", self.time)
			#t = tStudent.rvs(3)
			t = 60*chi2.rvs(3)
			self.listEvents.addEvent("UnloadingDone", self.time + t, oilTanker)
			self.oilTankersWharves.append(oilTanker)
		elif self.detectBlockedSituation():
			print "Blocked situation. I don't kow how to handle it."
			self.printState()
			self.printResultsOnTheFly()
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
		
		if self.freeTugs > 0 and self.listEvents.getListEventSize("ArrivalTugWharf") < len(self.oilTankersWharvesDone) :
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
		ot = self.oilTankersWharvesDone.pop(0) #self.oilTankersWharvesDone[0]
		#self.oilTankersWharvesDone.remove(ot)  # = self.oilTankersWharvesDone[1:]
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
		self.maxTimeOilTankerInside = max(self.maxTimeOilTankerInside, self.time - oilTanker.getEntranceTime())
		if self.maxTimeOilTankerInside > 10000:
			print "Pause: " + str(len(oilTanker.listTimes))
			print "Pause: " + str(oilTanker)
			raw_input()
	
	def routineTugAvailable(self):
		"""
		Routine supposed to be triggered when a tug becomes available.
		Gives priority to coming oil tankers over oil tankers that are done 
		unloading.
		If a tug becomes available while there are some oil tankers waiting in 
		the entrance, the tug will take care of them (i.e. adds an event 
		"ArrivalTugEntrance" to the list).
		If a tug becomes available while the queue at the entrance is empty, 
		and an oil tanker is done at the wharves, the tug will go to the wharves 
		(i.e. adds an event "ArrivalTugWharf" to the list).
		Otherwise, the tug becomes available for further use.
		"""
		if len(self.oilTankersEntrance) > 0 and self.listEvents.getListEventSize("ArrivalTugEntrance") < len(self.oilTankersEntrance) :
			t = random.normalvariate(self.muEmpty, self.sigEmpty)
			self.listEvents.addEvent("ArrivalTugEntrance", self.time + t)
		elif len(self.oilTankersWharvesDone) > 0 and self.listEvents.getListEventSize("ArrivalTugWharf") < len(self.oilTankersWharvesDone) :
			t = random.normalvariate(self.muEmpty, self.sigEmpty)
			self.listEvents.addEvent("ArrivalTugWharf", self.time + t)
		elif self.freeTugs < self.maxTugs: # Should not occur, but well...
			self.freeTugs += 1
		
	def routineTugAvailableSafe(self):
		"""
		Routine supposed to be triggered when a tug becomes available.
		Gives priority to unloaded oil tankers over oil tankers that are coming 
		to the port.
		If a tug becomes available and an oil tanker is done at the wharves, 
		the tug will go to the wharves (i.e. adds an event "ArrivalTugWharf" 
		to the list).
		If a tug becomes available while there are some oil tankers waiting in 
		the entrance and no oil tanker is waiting at the wharves, the tug will 
		take care of them (i.e. adds an event "ArrivalTugEntrance" to the list).
		Otherwise, the tug becomes available for further use.
		"""
		if len(self.oilTankersWharvesDone) > 0 and self.listEvents.getListEventSize("ArrivalTugWharf") < len(self.oilTankersWharvesDone) :
			t = random.normalvariate(self.muEmpty, self.sigEmpty)
			self.listEvents.addEvent("ArrivalTugWharf", self.time + t)
		elif len(self.oilTankersEntrance) > 0 and self.listEvents.getListEventSize("ArrivalTugEntrance") < len(self.oilTankersEntrance) :
			t = random.normalvariate(self.muEmpty, self.sigEmpty)
			self.listEvents.addEvent("ArrivalTugEntrance", self.time + t)
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
	
	
	def getNumOilTankersInside(self):
		"""
		Returns the number of oil tankers inside the port.
		"""
		return self.listEvents.getNumTankers("ArrivalOilTankerWharf") + self.listEvents.getNumTankers("ExitOilTanker") + len(self.oilTankersWharves) + len(self.oilTankersWharvesDone)
			
			
	def updateTimes(self):
		"""
		Updates inner variables in anticipation of the results.
		"""
		intervalTime = self.time - self.previousTime
		
		self.meanNumOilTankersEntrance += float(len(self.oilTankersEntrance))*intervalTime
		self.maxNumOilTankersEntrance = max(len(self.oilTankersEntrance), self.maxNumOilTankersEntrance)
		
		tampon = float(self.getNumOilTankersInside())
		
		self.meanNumOilTankersInside += tampon * intervalTime
		self.maxNumOilTankersInside = max(tampon, self.maxNumOilTankersInside)
		
		self.meanTimeOilTankerInside += tampon * intervalTime
		#self.maxTimeOilTankerInside = 0.0 # I don't know how to update this one. Needs to be updated in routineExitOilTanker
		
		self.meanTimeOilTankersUnloading += len(self.oilTankersWharves) * intervalTime
		self.maxTimeOilTankersUnloading = max(float(len(self.oilTankersWharves)), self.maxTimeOilTankersUnloading)
		
		self.meanNumOilTankersWharves += (len(self.oilTankersWharves) + len(self.oilTankersWharvesDone)) * intervalTime
		self.maxNumOilTankersWharves = max(len(self.oilTankersWharves) + len(self.oilTankersWharvesDone), self.maxNumOilTankersWharves)
		
		
	def lastUpdateTimes(self):
		"""
		Updates a last time all the values, and calculates the means.
		"""
		self.updateTimes()
		
		self.meanNumOilTankersEntrance /= self.time
		self.meanNumOilTankersInside /= self.time
		self.meanTimeOilTankersUnloading /= self.time
		self.meanNumOilTankersWharves /= self.time
		self.meanTimeOilTankerInside /= self.time
		
		
	def printResults(self):
		"""
		Prints the results of the simulation.
		"""
		print "--------------------------------------------"
		print "Results of the simulation:"
		print "Mean number of oil tankers waiting in the entrance: " + str(self.meanNumOilTankersEntrance)
		print "Max number of oil tankers waiting in the entrance: " + str(self.maxNumOilTankersEntrance)
		print "Mean number of oil tankers inside the port: " + str(self.meanNumOilTankersInside)
		print "Max number of oil tankers inside the port: " + str(self.maxNumOilTankersInside)
		print "Mean time spent by the tankers inside the port: " + str(self.meanTimeOilTankerInside)
		print "Max time spent by the tankers inside the port: " + str(self.maxTimeOilTankerInside)
		print "Mean time spent by the tankers unloading at the wharves: " + str(self.meanTimeOilTankersUnloading)
		print "Max time spent by the tankers unloading at the wharves: " + str(self.maxTimeOilTankersUnloading)
		print "Mean number of tankers at the wharves: " + str(self.meanNumOilTankersWharves)
		print "Max number of tankers at the wharves: " + str(self.maxNumOilTankersWharves)
		print "Number of times the port was blocked: " + str(self.numTimesBlocked)
		print "--------------------------------------------"
		
	def printResultsOnTheFly(self):
		"""
		Computes and prints the results of the simulation if it were to stop now.
		"""
		print "--------------------------------------------"
		print "Results of the simulation:"
		print "Mean number of oil tankers waiting in the entrance: " + str(self.meanNumOilTankersEntrance/self.time)
		print "Max number of oil tankers waiting in the entrance: " + str(self.maxNumOilTankersEntrance)
		print "Mean number of oil tankers inside the port: " + str(self.meanNumOilTankersInside/self.time)
		print "Max number of oil tankers inside the port: " + str(self.maxNumOilTankersInside)
		print "Mean time spent by the tankers inside the port: " + str(self.meanTimeOilTankerInside/self.time)
		print "Max time spent by the tankers inside the port: " + str(self.maxTimeOilTankerInside)
		print "Mean time spent by the tankers unloading at the wharves: " + str(self.meanTimeOilTankersUnloading/self.time)
		print "Max time spent by the tankers unloading at the wharves: " + str(self.maxTimeOilTankersUnloading)
		print "Mean number of tankers at the wharves: " + str(self.meanNumOilTankersWharves/self.time)
		print "Max number of tankers at the wharves: " + str(self.maxNumOilTankersWharves)
		print "Number of times the port was blocked: " + str(self.numTimesBlocked)
		print "--------------------------------------------"
		
		
	@staticmethod	
	def printList(st, li):
		s = st + "["
		for i in li:
			s += str(i) + ", "
		s += "], size: " + str(len(li))
		print s
		
	def printState(self):
		print "/\\_/\\_/\\_/\\_/\\_/\\_/\\_/\\_/\\_/\\_/\\_/\\_"
		print "Current state:"
		print "Time: " + minutesToTime(self.time) + " (" + str(self.time) + ")"
		print "Tankers generated: " + str(self.tankerCountTotalGenerated)
		print "Tankers handled: " + str(self.tankerCountDone)
		print "FreeTugs: " + str(self.freeTugs)
		print "Num times blocked: " + str(self.numTimesBlocked)
		print ""
		print self.listEvents
		print "All lists: "
		print self.printAllLists()
		
	def printAllLists(self):
		Port.printList("otEntrance: ", self.oilTankersEntrance)	
		Port.printList("otWharves: ", self.oilTankersWharves)	
		Port.printList("otWDone: ", self.oilTankersWharvesDone)	
		
		
	def detectBlockedSituation(self):
		blocked = (self.freeTugs == 0 and self.listEvents.getListEventSize("ArrivalTugWharf") == 0)
		blocked = blocked and (len(self.oilTankersWharves) + len(self.oilTankersWharvesDone) >= self.maxWharves)
		blocked = blocked and (self.listEvents.getListEventSize("TugAvailable") == 0)
		blocked = blocked and (self.listEvents.getListEventSize("ExitOilTanker") == 0)
		return blocked
		
		
		
		
		
		
		
		