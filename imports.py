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

import os
import re

''' 
Which imports do I need and where to find them
Theoretisch müsste, das rekursiv für alle Module gemacht werden (wenn cython-build erwünscht)
''' 

result = set()
for dirpath, dnames, fnames in os.walk("./"):
	for file in fnames:
		if file.endswith(".py") and '__init__' not in file:
			filename = os.path.join(dirpath, file)
			f = open(filename, 'r')
			for line in f:
				content = line.strip()
				m = re.search('(?<=^import )([a-zA-Z, ]+)', content)
				if m:
					for x in m.group(0).split(','):
						result.add(x.strip())
				n = re.search('(?<=^from )([a-zA-Z,\.]+)', content)
				if n:
					result.add(n.group(0))

#for name, m in zip(result, map(__import__, result)):
for name in sorted(result):
	try:
		m = __import__(name, globals=globals())
		print("%25s: %s" % (name, m.__file__))
	except ImportError:
		print("%25s: %s" % (name, "Module not found."))
	except AttributeError:
		print("%25s: %s" % (name, m))
	#except:
	#	print("%25s: [ERR] Module not found!" % name)