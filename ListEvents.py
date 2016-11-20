# -*- coding:utf8 -*-


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
		self.tankers = {"ArrivalOilTankerEntrance": [],
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
			oilTanker	In the special case in which the event is an "UnloadingDone", 
						we need to know which tanker is concerned.
		"""
		self.events[event].append(time)
		
		if event in tankers.keys():
			if oilTanker not None:
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
		the event and the time at which it's supposed to occur.
		
		"""
		minEvent = ""
		minTime = 0.0
		minOilTanker = None
		
		for key, value in self.events:
			if len(value) > 0 and value[0] < minTime:
				minEvent = key
				minTime = value[0]
				if key in self.tankers.keys():
					minOilTanker = self.tankers[key][0]
		
		return minEvent, minTime
	
	
	def removeLastEvent(self, event):
		"""
		Removes the first time of given "event".
		
		Arguments:
			event		The event the first time of which should be removed.
		"""
		self.events[event] = self.events[event][1:]
		if event in self.tankers.keys():
			self.tankers[event] = self.tankers[event][1:]

