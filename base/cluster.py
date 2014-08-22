#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2014 Alexander Bredo
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or 
# without modification, are permitted provided that the 
# following conditions are met:
# 
# 1. Redistributions of source code must retain the above 
# copyright notice, this list of conditions and the following 
# disclaimer.
# 
# 2. Redistributions in binary form must reproduce the above 
# copyright notice, this list of conditions and the following 
# disclaimer in the documentation and/or other materials 
# provided with the distribution.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND 
# CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, 
# INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF 
# MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE 
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR 
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, 
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES 
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE 
# GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR 
# BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF 
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT 
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT 
# OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE 
# POSSIBILITY OF SUCH DAMAGE.

import math

'''
TODO:
 - Fließende Berechnung der Standardabweichung bei sehr langen Listen mit gleichverteilten Daten implementieren 
   (Bsp: range(1,100) + range(106,200))
   Idee: die berechnete Varianz zwischenspeichern und dann 10% (?) vorher und nachher für die Berechnung der Standardabweichung berücksichtigen. Globale StdAbw ist auf jeden Fall eine Gruppentrennung. Lokale Varianz (optional)? -- Es könnten vllt zu viele Gruppen entstehen.
'''

class TimeBasedCluster():
	def __init__(self, inlist):
		self.inlist = inlist
		
	def clusterize(self):
		stdDev = self.__std(self.inlist)
		result = []
		tempgroup = []
		for idx, val in enumerate(self.inlist):
			tempgroup.append(val)
			if (idx+1 < len(self.inlist)):
				if ((val - self.inlist[idx+1]) ** 2) >= stdDev:
					result = result + [tempgroup]
					tempgroup = [] # neue Gruppe
			else:
				result = result + [tempgroup] # letzter Durchlauf
		return result
		
	def clusterize_compact(self, minclustersize=1):
		oldcluster = self.clusterize()
		
		if len(oldcluster) < 2:
			return oldcluster # nothing to do
		
		# first, append to next, remove first
		if len(oldcluster[0]) <= minclustersize:
			oldcluster[1] = oldcluster[0] + oldcluster[1]
			del(oldcluster[0])
		
		# last, append to previous, remove last
		if len(oldcluster[-1]) <= minclustersize:
			oldcluster[-2] = oldcluster[-2] + oldcluster[-1]
			del(oldcluster[-1])
		
		# center, append to near(n/p)
		for i,x in enumerate(oldcluster):
			if (len(x) <= minclustersize):
				if (min(x) - max(oldcluster[i - 1])) < (min(oldcluster[i + 1]) - max(x)):
					oldcluster[i - 1] = oldcluster[i - 1] + x
				else:
					oldcluster[i + 1] = x + oldcluster[i + 1]
				del(oldcluster[i])
		return oldcluster
		
	def cluster_boundaries(self, cluster):
		return [dict(min=min(x), max=max(x), count=len(x), bandwidth=(max(x)-min(x))) for x in cluster]
		
	def __std(self, valuelist): # Standardabweichung
		return math.sqrt(self.__var(valuelist))
		
	def __var(self, valuelist): # Varianz
		avg = self.__exp(valuelist)
		return self.__exp([(x - avg) ** 2 for x in valuelist])
		
	def __exp(self, valuelist): # Erwartungswert
		return float(sum(valuelist)) / len(valuelist)
		
if __name__ == '__main__':
	a = [1, 5, 5, 7, 14, 20, 21]
	#a = range(1,100) + range(106,200)
	tbc = TimeBasedCluster(a)
	print(tbc.clusterize())
	print(tbc.clusterize_compact(2))
	print(tbc.cluster_boundaries(tbc.clusterize_compact()))