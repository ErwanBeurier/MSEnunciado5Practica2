# -*- coding:utf8 -*-


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
	
	def getTotalTime(self):
		return self.totalTime
		
		
		
		
		
		
		
		
		
		
		
		
		
	