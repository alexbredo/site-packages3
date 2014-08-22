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

# -*- coding: utf-8 -*-

'''
Download: https://standards.ieee.org/develop/regauth/oui/oui.txt
'''
import re, os
from bisect import bisect_left

class MACVendor():
	def __init__(self, ouifile=None):
		# If no path given, then try same directory as script
		if not ouifile:
			ouifile = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'oui.txt')
		
		self.data = []
		self.keys = []
		f = open(ouifile, 'r', encoding="latin1")
		for line in f:
			result = self.__extractMacVendor(line)
			if result:
				self.data.append(result)
				self.keys.append(result[0])

	def __extractMacVendor(self, line):
		# line ~= "  001B17     (base 16)		Palo Alto Networks"
		p = re.compile("(?:[\s\t]+)([0-9a-fA-F:]{6})(?:[\s\t]+)(?:\(base 16\))(?:[\s\t]+)(.+)")
		m = p.match(line)
		if m:
			macaddr, vendor = m.groups()
			macaddr = int(macaddr, 16)
			return (macaddr, vendor)
		else:
			return None
			
	def lookupVendorByNum(self, macaddrnum):
		try:
			result = self.data[bisect_left(self.keys, macaddrnum)]
			if macaddrnum == result[0]:
				return result[1]
			return None
		except IndexError:
			return None
			
	'''
		Valid Input Formats:
		000C87
		00-0C-87
		00:0C:87
		000C87112233
		00-0C-87-11-22-33
		00:0C:87:11:22:33
	'''
	def lookupVendor(self, macaddr):
		macaddr = macaddr.replace(':', '').replace('-', '').strip()
		if len(macaddr) > 12 or len(macaddr) < 6:
			raise Exception("Possibly invalid MAC-Address specified (%s)" % macaddr)
		return self.lookupVendorByNum(int(macaddr[:6], 16))
		
if __name__ == '__main__':
	m = MACVendor()
	print(m.lookupVendor('28:ba:b5'))