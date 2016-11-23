# -*- coding:utf8 -*-


"""============================================================================
								ENUNCIADO 5
								PRACTICA 2
								
	BEURIER Erwan
	CANAVATE VEGA Fernando
	DE LA ROSA Augustin
	NAPOLI Luca 

	This file contains the implementation of the class ListEvents.
	
	Useful methods:
		addEvent()
		getNextEvent()
		removeLastEvent()
	(The rest is supposed to be private, even if Python doesn't know about 
	encapsulation)
	
	This file is not supposed to be launched via console.
	
	
	Vocabulary (because the code is in English but the wording is in Spanish):
		tug 		= remolcador
		oil tanker	= petrolero
		wharf 		= muelle
	
	
TODO:

============================================================================"""


import OilTanker

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
		tankers			Dictionary (events, list of tankers). Contains the 
						tankers corresponding to the event.
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
		self.tankers = {"ArrivalOilTankerEntrance": [], # Ill-named. Should be understood as "Oil Tankers Waiting in the entrance"
						"ArrivalOilTankerWharf": [],
						"UnloadingDone": [],
						"ExitOilTanker": [],
						}
	
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
			oilTanker	In the special case in which the event concerns an oil 
						tanker, we need to know which tanker is concerned.
		"""
		self.events[event].append(time)
		
		if event in self.tankers.keys():
			if oilTanker is not None:
				oilTanker.addTime(time, False)
				self.tankers[event].append(oilTanker)
				ListEvents.doubleMergeSort(self.events[event], self.tankers[event])
			else:
				raise Exception(event + " without specified tanker. Abort.")
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
		the event, the time at which it's supposed to occur, and potentially the 
		oil tanker that is concerned.
		"""
		minEvent = ""
		minTime = 1000000.0
		minOilTanker = None
		
		for key, value in self.events.iteritems():
			if len(value) > 0 and value[0] < minTime:
				minEvent = key
				minTime = value[0]
				if key in self.tankers.keys():
					minOilTanker = self.tankers[key][0]
		return minEvent, minTime, minOilTanker
	
	
	def removeLastEvent(self, event):
		"""
		Removes the first time of given "event".
		
		Arguments:
			event		The event the first time of which should be removed.
		"""
		self.events[event].pop(0)# = self.events[event][1:]
		if event in self.tankers.keys():
			#self.tankers[event] = self.tankers[event][1:]
			self.tankers[event].pop(0) #.remove(self.tankers[event][0])

	@staticmethod
	def strDico(dico):
		s = ""
		for key, value in dico.iteritems():
			s = s + "\r\n  " + str(key) + ": " + ListEvents.strList(value)
		return s
	
	@staticmethod
	def strList(lis):
		s = "["
		for pouet in lis:
			s += str(pouet)+ ", "
		s += "]"
		return s
	
	def __str__(self):
		s = "self.events: \r\n" + ListEvents.strDico(self.events) 
		s += "\r\nself.tankers: \r\n" + ListEvents.strDico(self.tankers)
		return s
				
		
	def getNumTankers(self, event):
		return len(self.tankers[event])
		
	def getListEventSize(self, event):
		return len(self.events[event])
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		