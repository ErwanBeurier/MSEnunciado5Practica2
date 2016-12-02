# -*- coding:utf8 -*-


"""============================================================================
								ENUNCIADO 5
								PRACTICA 2
								
	BEURIER Erwan
	CANAVATE VEGA Fernando
	DE LA ROSA Augustin
	NAPOLI Luca 

	This file contains the implementation of the class OilTanker.
	
	Useful methods:
		getTotalTime()
		addTime()
	(The rest is supposed to be private, even if Python doesn't know about 
	encapsulation)
	
	This file is not supposed to be launched via console.
	
	Vocabulary (because the code is in English but the wording is in Spanish):
		oil tanker	= petrolero
	

============================================================================"""


from math import log


class OilTanker:
	"""
	Convenient class. 
	Stores the time spent in the port.
	
	Attributes:
		id				The id of the oil tanker. To identify the oil tanker.
		arrivalTime		Arrival time of the boat at the port.
		lastTimeTookCare	Last time we took care of this ship.
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
			id			The id of the oil tanker.
			t 			The arrival time at the entrance of the port.
		"""
		self.id = id
		self.arrivalTime = t
		self.entranceTime = t
		self.lastTimeTookCare = t
		self.lastInterval = 0
		self.totalTime = 0.0
		self.listTimes = [0.0]
		
		
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
		t1 = t
		
		if not interval:
			t1 = t - self.lastTimeTookCare
			
		self.listTimes.append(t1)
		self.totalTime += t1
		self.lastTimeTookCare += t1
		self.lastInterval = t1 	
	
	
	
	
	"""========================================================================
	Below these two lines are functions that are not crucial to the 
	understanding of the code.
	========================================================================"""

	def __hash__(self):
		"""
		To make the oil tanker hashable. Simply returns its id. 
		"""
		return self.id
		
	def __eq__(self, other):
		"""
		A comparison function. Mandatory to be able to remove an oil tanker from 
		a list in ListEvents or in Port classes.
		"""
		if isinstance(other, OilTanker):
			return (other.id == self.id)
		
		return False
		
	def __str__(self):	
		"""
		Method to make the instance printable.
		"""
		#return "Oil Tanker num " + str(self.id) + " arrived at " + str(self.arrivalTime)
		return "OT" + "0"*(4- int(log(self.id, 10))) + str(self.id)
		
	
	def getTotalTime(self):
		"""
		Accessor method. Not needed in Python but still a good practice.
		"""
		return self.totalTime
		
		
	def getLastTimeTookCare(self):
		"""
		Accessor method.
		"""
		return self.lastTimeTookCare
		
	
	def getLastInterval(self):
		"""
		Accessor method.
		"""
		return self.lastInterval
		
	def getEntranceTime(self):
		"""
		Accessor method.
		"""
		return self.arrivalTime + self.listTimes[1]

		
		
		
		
	