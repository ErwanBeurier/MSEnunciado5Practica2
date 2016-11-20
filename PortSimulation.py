# -*- coding:utf8 -*-

import random
from enum import Enum
from scipy.stats import t as tStudent
from scipy.stats import norm


class ListEvents:
	"""
	Class containing the information about the different events that can occur 
	in the simulation.
	The events are stored in a dictionary. The key is the name of the event, 
	and the associated value is a list of float, supposed to be the times (in 
	minutes).
	The Port is supposed to contain one instance of this class.
	
	Attributes:
		events			Dictionary (events, list of times). The events are 
						supposed to occur at the times given in the list.
	"""
	def __init__(self):
		"""
		Default initializer. Empty list for every event.
		"""
		self.events = {"ArrivalOilTankerEntrance": [],
						"ArrivalTugEntrance": [],
						"ArrivalOilTankerWharf": [],
						"UnloadingDone": [],
						"ArrivalTugWharf": [],
						"ExitOilTanker": [],
						"TugAvailable": []
						}
		self.tankers = []
	
	
	def addEvent(self, event, time, oilTanker = None):
		"""
		Adds the event "event" at given "time". Sorts the list of times of the 
		given event, so the first element of the list is always the soonest to 
		come.
		
		Arguments:
			event		The code of the event. Cf. __init__() to see what 
						events make sense in this simulation.
			time 		Time in minutes. The timestamp at which the event is 
						supposed to occur.
			oilTanker	In the special case in which the event is an "UnloadingDone", 
						we need to know which tanker is concerned.
		"""
		self.events[event].append(time)
		
		if event == "UnloadingDone":
			if oilTanker not None:
				self.tankers.append(oilTanker)
				ListEvents.doubleMergeSort(self.events[event], self.tankers)
			else:
				raise Exception("UnloadingDone without specified tanker. Abort.")
				return 
		else:
			self.events[event].sort()
 
 
	@staticmethod
	def doubleMergeSort(liUnloaded, tankers):
		"""
		Applies a merge sort on both lists. However, the values of "liUnloaded" 
		are the only one used to sort both lists. It means that "tankers" is 
		supposed to be paired.
		
		Arguments:
			liUnloaded		A list to sort. 
			tankers			Second list to sort. 
		"""
		if len(liUnloaded) > 1:
			mid = len(liUnloaded)//2
			leftList = liUnloaded[:mid]
			rightList = liUnloaded[mid:]
			leftTankers = tankers[:mid]
			rightTankers = tankers[mid:]

			ListEvents.doubleMergeSort(leftList, leftTankers)
			ListEvents.doubleMergeSort(rightList, rightTankers)

			i = 0
			j = 0 
			k = 0
			while i < len(leftList) and j < len(rightList):
				if leftList[i] < rightList[j]:
					liUnloaded[k] = leftList[i]
					tankers[k] = leftTankers[i]
					i += 1
				else:
					liUnloaded[k]=rightList[j]
					tankers[k] = rightTankers[j]
					j += 1
				k += 1

			while i < len(leftList):
				liUnloaded[k] = leftList[i]
				tankers[k] = leftTankers[i]
				i += 1
				k += 1

			while j < len(rightList):
				liUnloaded[k] = rightList[j]
				tankers[k] = rightTankers[j]
				j += 1
				k += 1
	
	def getNextEvent(self):
		"""
		Searches the attribute "events" to find the next event to come. Returns 
		the event and the time at which it's supposed to occur.
		
		"""
		minEvent = ""
		minTime = 0.0
		
		for key, value in self.events:
			if len(value) > 0 and value[0] < minTime:
				minEvent = key
				minTime = value[0]
				
		return minEvent, minTime
	
	
	def removeLastEvent(self, event):
		"""
		Removes the first time of given "event".
		
		Arguments:
			event		The event the first time of which should be removed.
		"""
		self.events[event] = self.events[event][1:]


class OilTanker:
	"""
	Convenient class. 
	Stores the time spent in the port.
	
	Attributes:
		arrivalTime		Arrival time of the boat at the port.
		listTimes		List of times spent in the port. It's not a list of 
						timestamps, but a list of times spent (it's not a list 
						of absolute times).
						NB: I've put a list because their are lots of things to 
						check to answer the question. We could register every 
						action of the boat and check this list to decompose its 
						travel.
		totalTime		Total time spent by the OilTanker in the Port.
	"""
	
	def __init__(self, t, id):
		"""
		Default constructor. 
		
		Arguments:
			t 			The arrival time at the entrance of the port.
		
		"""
		self.totalTime = 0.0
		self.listTimes = [0.0]
		self.arrivalTime = t
		self.lastTimeTookCare = t # Last time we took care of this ship.
		self.id = id
		
	def __hash__(self):
		return self.id
		
	def __eq__(self, other):
		if isinstance(other, OilTanker):
			return (other.id == self.id)
		
		return False
		
		
	def addTime(self, t, interval = True):
		"""
		Registers a new time in the instance. 
		
		Arguments:
			t 			Interval of time between the last event and the recorded 
						event (if "interval" is True) OR timestamp of last event 
						occuring to this boat.
			interval 	Defines the sense of the argument "t" : interval of time 
						or timestamp.
		"""
		
		if interval:
			self.listTimes.append(t)
			self.totalTime += t
			self.lastTimeTookCare += t
		else:
			t1 = t - self.lastTimeTookCare
			self.listTimes.append(t1)
			self.totalTime += t1
			self.lastTimeTookCare += t1
	
	
class Port:
	"""
	The class managing the port.
	
	Attributes:
		maxWharves
		maxTugs
		oilTankersEntrance		"Petroleros en la entrada". Queue in the entrance. No limit on size.
		oilTankersWharves		"Petroleros en un muelle". List of oil tankers at the wharves. Should be limited.
		freeTugs
		time					Timestamp.
		maxTime
	"""
	
	
	def __init__(self, maxWharves, maxTugs, timeSimulation, muEmpty = 2, sigEmpty = 1, muFull = 10, sigFull = 3):
		"""
		Constructor. 
		
		Arguments:
			maxWharves			The maximum number of wharves in the port.
			maxTugs				The maximum number of tugs in the port.
			timeSimulation		The duration of the simulation.
		"""
		self.maxWharves = maxWharves
		self.maxTugs = maxTugs
		self.oilTankersEntrance = [] # No limit on size.
		self.oilTankersWharves = [] # Needs to be of size <= maxWharves
		self.oilTankersWharvesDone = [] # The indices in oilTankerWharves that have finished unloading.
		self.freeTugs = maxTugs # size <= maxTugs
		self.time = 0.0
		self.maxTime = timeSimulation
		self.listEvents = ListEvents()
		self.muEmpty = muEmpty
		self.sigEmpty = sigEmpty
		self.muFull = muFull
		self.sigFull = sigFull
	
	def simulate(self):
		
		"""
		So it will be a while loop 
			while 
				get first event
				if event = pouet1:
					dfkfjlskdf
				elif event = pouet2:
					<lkdjfml<
				etc.
		"""
		
		
	def generateOilTanker(self):
		"""
		Used to generate an OilTanker. Simulates an exponential variate of 
		parameter Port.lambdat, adds the OilTanker to the list of events.
		"""
		t = random.expovariate(Port.lambdat(self.time))
		self.oilTankersEntrance.append(OilTanker(t))
		self.listEvents.addEvent("ArrivalOilTankerEntrance", self.time + t)
		
	
	
	@staticmethod
	def lambdat(t):
		"""
		Generates the lambda depending on the time "t".
		"""
		t = t % 24.0
		lt = 0
		if 0.0 <= t and t < 5.0:
			lt = 2.0/5.0*t - 5.0
		elif 5.0 <= t and t < 9.0:
			lt = -1.0/4.0*t - 33.0/4
		elif 9.0 <= t and t < 15.0:
			lt = 1.0/2.0*t - 3.0/2.0
		elif 15.0 <= t and t < 17.0:
			lt = -3.0/2.0*t - 63.0/2.0
		else:
			lt = -1.0/7.0*t - 59.0/7.0
		return lt
	
	
	def routineArrivalOilTankerEntrance(self):
		
	
	
	def routineArrivalTugEntrance(self):
	
	
	
	def routineArrivalOilTankerWharf(self):
		"""
		Wait ??? 
		There can be a blocked situation here!
		If: the wharves are full 
			+ the oilTankers in the wharves need a tug to exit the wharves 
			+ the tugs are carrying an oil tanker to the wharves
		
		"""
		self.routineTugAvailable() # After the tug has left the oil tanker at the wharf!
		
	
	
	def routineUnloadingDone(self):
		if self.freeTugs > 0:
			t = random.normalvariate(self.muEmpty, self.sigEmpty)
			self.listEvents.addEvent("ArrivalTugWharf", self.time + t)
		else:
			self.oilTankersWharvesDone()
	
	
	def routineArrivalTugWharf(self):
		
	
	
	def routineExitOilTanker(self):
		
	
	
	def routineTugAvailable(self):
		if len(self.oilTankersEntrance) > 0:
			t = random.normalvariate(self.muEmpty, self.sigEmpty)
			self.listEvents.addEvent("ArrivalTugEntrance", self.time + t)
		elif len(self.oilTankersWharvesDone) > 0:
			t = random.normalvariate(self.muEmpty, self.sigEmpty)
			self.listEvents.addEvent("ArrivalTugWharf", self.time + t)
		elif self.freeTugs < self.maxTugs:
			self.freeTugs += 1

		
		
		
# self.events = {"ArrivalOilTankerEntrance": [],
				# "ArrivalTugEntrance": [],
				# "ArrivalOilTankerWharf": [],
				# "UnloadingDone": [],
				# "ArrivalTugWharf": [],
				# "ExitOilTanker": [],
				# "TugAvailable": []
				# }
		
		
		
		
		
		
		
		
		
		
		