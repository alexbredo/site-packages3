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

from base.applog import *
import urllib3
import json
from base.text import clean

'''
TODO:
 - BUG: Illegal unquoted character ((CTRL-CHAR, code 8)): has to be escaped using backslash to be included in string value
'''

class ElasticsearchClient():
	def __init__(self, host='127.0.0.1', port=9200, index='default', doctype='doc', ttl='1w'):
		self.http = urllib3.PoolManager()
		self.index = index
		self.doctype = doctype
		self.host = host
		self.port = port
		self.ttl = ttl
		self.setup()
		
	def setup(self):
		if not self.exists_index():
			log.info("Elasticsearch-Index '%s' does not exist. Trying to create now." % self.index)
			self.create_index_mapping()
		else:
			log.info("Elasticsearch-Index '%s' present." % self.index)
		
	def saveOne(self, data, doctype):
		nice_data = json.dumps(clean(data), indent=4, separators=(',', ': '))
		r = self.http.urlopen('POST', 
			'http://%s:%i/%s/%s' % (self.host, self.port, self.index, doctype), 
			headers = {'Content-Type':'application/json'},
			body = nice_data
		)
		print (r.status, r.data)
		if int(r.status/100) == 2:
			log.debug("Element %s has been saved." % nice_data)
		else:
			log.error("Element could not be saved: %s. Error: %s" % (nice_data, r.data))

	def saveMany(self, data, doctype):
		log.debug("Trying to save %d items to Elasticsearch." % len(data))
		serialized_data = [self.__makeStringsFromDict(x) for x in data]
		head = ({ "index" : { "_index" : self.index, "_type" : doctype } }).__str__() + '\n'
		dataAsStr = ('\n'.join([head + line.__str__() for line in serialized_data])).replace('\'', '\"') + '\n'
		
		r = self.http.urlopen('POST', 
			'http://%s:%i/%s/%s/_bulk' % (self.host, self.port, self.index, doctype),
			headers = {'Content-Type':'application/json'},
			body = dataAsStr
		)
		if int(r.status/100) == 2:
			log.debug("%s Elements has been saved." % len(data))
		else:
			log.error("Elements could not be saved: %s. Error: %s" % (dataAsStr, r.data))
	
	def __makeStringsFromDict(self, dictionary):
		try:
			for key in dictionary.keys():	# Native Datatypes: No Objects!
				if isinstance(dictionary[key], dict): # nested...
					dictionary[key] = self.__makeStringsFromDict(dictionary[key])
				elif isinstance(dictionary[key], str):
					dictionary[key] = dictionary[key].__str__()
				#elif isinstance(dictionary[key], int) and isinstance(dictionary[key], float):
				#	dictionary[key] = dictionary[key]
			return dictionary
		except Exception as e:
			log.error(e)

	def deleteIndex(self):
		r = self.http.request('DELETE', 'http://%s:%i/%s/' % (self.host, self.port, self.index))
		if int(r.status/100) == 2:
			log.info("Elasticsearch-Index '%s' was removed." % self.index)
			return True
		else:
			log.warning("Elasticsearch-Index '%s' does not exist." % self.index)
			return False # print r.data
			
	def exists_index(self):
		r = self.http.request('GET', 'http://%s:%i/%s/_mapping' % (self.host, self.port, self.index))
		if int(r.status/100) == 2:
			return True
		else:
			return False # print r.data
		
	def create_index_mapping(self):
		# POST /index/
		data = """{
			"mappings" : {
				"_default_" : {
					"_ttl": {
					   "enabled": "true",
					   "default": "%s"
					},
					"properties" : {
						"sourceIPv6Address": { "type": "string", "index": "not_analyzed" },
						"destinationIPv6Address": { "type": "string", "index": "not_analyzed" },
						"sourceHostname" : {"type" : "string", "index" : "not_analyzed"},
						"destinationHostname" : {"type" : "string", "index" : "not_analyzed"},
						"destinationTransportPortName" : {"type" : "string", "index" : "not_analyzed"},
						"sourceTransportPortName" : {"type" : "string", "index" : "not_analyzed"},
						"protocolIdentifierName" : {"type" : "string", "index" : "not_analyzed"},
						"networkLocation" : {"type" : "string", "index" : "not_analyzed"},
						"command" : {"type" : "string", "index" : "not_analyzed"},
						"session" : {"type" : "string", "index" : "not_analyzed"}
					}
				}
			}
		}""" % self.ttl
		r = self.http.urlopen('POST', 
			'http://%s:%i/%s/' % (self.host, self.port, self.index), 
			headers = {'Content-Type':'application/json'},
			body = data
		)
		if int(r.status/100) == 2:
			log.info("Elasticsearch-Index '%s' has been created." % self.index)
		else:
			log.error("Elasticsearch-Index '%s' has NOT been created. (%s)" % (self.index, r.data))

if __name__ == '__main__':
	ec = ElasticsearchClient('lnx06-elasticsearch1', 9200, 'honeypot')
	ec.deleteIndex()
	#ec.saveOne({'ab':1, 'cd':'blub'}, 'intrusion')
	#ec.saveMany([{'ab':1, 'cd':'blub'}, {'ddd':22, 'dfd':'fdgg'}], 'intrusion')