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

# ä 196 228 ö 214 246 ü 220 252
special_german_umlaute = [ord(u'ä'), ord(u'Ä'), ord(u'ö'), ord(u'Ö'), ord(u'ü'), ord(u'Ü')] 

def removeNonAscii(s): 
	# Source:  http://stackoverflow.com/questions/1342000/how-to-make-the-python-interpreter-correctly-handle-non-ascii-characters-in-stri
	return "".join(i for i in s if ord(i) < 128 or ord(i) in special_german_umlaute)
	
def removeNonAsciiWithoutControl(s): 
	return "".join(i for i in s if 32 <= ord(i) < 128 or ord(i) in special_german_umlaute)
	
def cleanString(s):
	# Removes multiple spaces/tabs/newlines, trailing spaces/tabs -- very fast vs re
	# Source: http://stackoverflow.com/questions/2077897/substitute-multiple-whitespace-with-single-whitespace-in-python
	return ' '.join(removeNonAsciiWithoutControl(s).split())
		
def applyFunction(s, func):
	if isinstance(s, str):
		return func(s)
	if isinstance(s, int) or isinstance(s, long):
		return s
	elif isinstance(s, dict):
		return dict((k, applyFunction(v, func)) for k,v in s.items())
	elif isinstance(s, list):
		return [applyFunction(v, func) for v in s]
	elif isinstance(s, tuple):
		return tuple(applyFunction(v, func) for v in s)
	else:
		return s # Rest nicht antasten
		
def clean(s):
	return applyFunction(s, cleanString)
	
if __name__ == '__main__':
	a = "\n\n\n Credentials: ÿýÿûÿûÿû   \n\n\nÿû!ÿûÿû'ÿýHEARTBEAT:HEARTBEAT  "
	b = {'a': '  bccäöüeê', 'v': 12}
	c = ('a', '\nhfksdhfäöä342/((   /%/§ê'), ('v', 12)
	print(type(c))
	print(clean(a))
	print(clean(b))
	print(clean(c))