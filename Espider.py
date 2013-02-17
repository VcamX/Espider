# -*- coding: utf-8 -*-
import StringIO
import lxml.html
from lxml import etree
import urllib2

class Espider():
	def __init__(self, url, code = "utf-8"):
		self.content = self.fetchContent(url, code)
		self.tree = self.buildTree(self.content)
	
	def fetchContent(self, url, code = "utf-8"):
		try:
			opener = urllib2.build_opener(urllib2.HTTPRedirectHandler(), urllib2.HTTPCookieProcessor())
			response = opener.open(url)
		except:
			return -1
		html = response.read()
		content = html.decode(code, "ignore")
		return content
	
	def buildTree(self, content):
		try:
			tree = lxml.html.parse(StringIO.StringIO(content))
		except:
			return -2
		return tree
	