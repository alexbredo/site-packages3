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

from handler.elasticsearch import ElasticsearchClient
from handler.file import FileWriter	
from base.applog import *

class HandlerManager():
	def __init__(self, config):
		self.enabled_handlers = config.enabled_handlers
		if self.enabled_handlers['elasticsearch']:
			self.es_client = ElasticsearchClient(
				config.elasticsearch['host'], 
				config.elasticsearch['port'], 
				config.elasticsearch['index']
			)
			log.info("Saving to Elasticsearch enabled. Destination: http://%s:%s/%s" % (
				config.elasticsearch['host'], 
				config.elasticsearch['port'], 
				config.elasticsearch['index']
			))
		if self.enabled_handlers['file']:
			self.file_writer = FileWriter(config.filename)
			log.info("Saving to File enabled. Filename: %s" % config.filename)
		if self.enabled_handlers['screen']:
			log.info("Output to Screen (STDOUT) enabled.")
		
	def handle(self, element, type='intrusion'):
		if self.enabled_handlers['elasticsearch']:
			self.es_client.saveOne(element, type)
		if self.enabled_handlers['file']:
			self.file_writer.append(element)
		if self.enabled_handlers['screen']:
			log.warning(element)
