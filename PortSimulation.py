# -*- coding:utf8 -*-

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
		self.tankerCountDone = 0
		self.tankerCountInside = 0
		self.tankerCountWaiting = 0
		self.cumulTimeTankersDone = 0.0
	
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
		self.tankerCountWaiting += 1

	
	
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
		
	
	
	def routineUnloadingDone(self, oilTanker):
		self.oilTankersWharves.remove(oilTanker)
		
		if self.freeTugs > 0:
			t = random.normalvariate(self.muEmpty, self.sigEmpty)
			self.listEvents.addEvent("ArrivalTugWharf", self.time + t)
		else:
			self.oilTankersWharvesDone.append(oilTanker)
			
	def routineArrivalTugWharf(self):
		t = random.normvariate(self.muFull, self.sigFull)
		self.listEvents.addEvent("ExitOilTanker", self.time + t, self.oilTankersWharvesDone[0])
	
	
	def routineExitOilTanker(self, oilTanker):
		# oilTanker.addTime(self.time, False) #Already done in addEvent?
		self.cumulTimeTankersDone = oilTanker.getTotalTime()
		self.tankerCountInside -= 1
		self.tankerCountDone += 1
		self.listEvents.addEvent("TugAvailable", self.time)
		
	
	def routineTugAvailable(self):
		if len(self.oilTankersEntrance) > 0:
			t = random.normalvariate(self.muEmpty, self.sigEmpty)
			self.listEvents.addEvent("ArrivalTugEntrance", self.time + t)
		elif len(self.oilTankersWharvesDone) > 0:
			t = random.normalvariate(self.muEmpty, self.sigEmpty)
			self.listEvents.addEvent("ArrivalTugWharf", self.time + t)
		elif self.freeTugs < self.maxTugs: # Should not occur, but well...
			self.freeTugs += 1
		
		
		
		
# self.events = {"ArrivalOilTankerEntrance": [],
				# "ArrivalTugEntrance": [],
				# "ArrivalOilTankerWharf": [],
				# "UnloadingDone": [],
				# "ArrivalTugWharf": [],
				# "ExitOilTanker": [],
				# "TugAvailable": []
				# }
		
		
		
		
		
		
		
		
		
		
		