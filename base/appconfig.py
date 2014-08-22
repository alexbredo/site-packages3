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

# Idee Config + Argumente in einem definieren
# die Argumente, die erwartet werden, auch in der Config suchen.
# + Sample Config Generator
# Prio: Argumente vor Config

import argparse, sys
from base.xmlserializer import Serializable
from base.applog import *

class Configuration(Serializable):
	# Override this function!
	def setup(self, *args, **kwargs):
		# Private:
		self.__version = '0.0.0'
		self.__appname = 'NO_APPNAME'
		# Defaults (Settings):
		# self.ipfix_port = 4739
		
	def __init__(self):
		Serializable.__init__(self, 'config.xml')
		#super(Configuration, self).__init__('config.xml')
		self.setup()
		#super(Configuration).__init__('config.xml')
		# Config File:
		self.__parseArguments()
		self.__handleArguments()
	
	def __parseArguments(self):
		ap = argparse.ArgumentParser(description="Dump IPFIX-Messages collected over UDP")
		ap.add_argument('-v', '--version', help='Print Version', action='store_true')
		ap.add_argument('-c', '--config', metavar='Configfile', help='Which config-file to use (default: config.xml)')
		ap.add_argument('-d', '--defaultconfig', metavar='Configfile', help='Write sample Config with default values')
		self.__args = ap.parse_args()
		
	def __handleArguments(self):
		if self.__args.version:
			print("%s. Version: %s" % (self.__appname, self.__version))
			print("(c) 2014 by Alexander Bredo, EDAG AG")
			sys.exit(0)
		if self.__args.defaultconfig:
			self._filename = self.__args.defaultconfig
			self.save()
			print("Default config has been generated. See %s" % self._filename)
			sys.exit(0)
		if self.__args.config:
			self._filename = self.__args.config
		try:
			self.load()
			log.info("Using %s as configuration." % self._filename)
		except Exception:
			log.info("Configuration file '%s' was not found. Using default values." % self._filename)