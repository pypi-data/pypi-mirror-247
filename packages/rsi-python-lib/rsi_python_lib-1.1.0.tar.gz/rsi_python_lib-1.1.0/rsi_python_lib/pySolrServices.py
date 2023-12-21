# -*- coding: utf-8 -*-

import logging
import urllib.request, urllib.error, urllib.parse
import base64
from xml.dom import minidom
import xml.etree.ElementTree as ET
import stat
import json
import os
from http.client import HTTPSConnection
from base64 import b64encode
import sys

# definizione dei namespaces per parsaqre gli atom
namespaces = { 'atom':'{http://www.w3.org/2005/Atom}',
	       'dcterms' : '{http://purl.org/dc/terms/}',
		'mam' : '{http://www.vizrt.com/2010/mam}',
		'opensearch' : '{http://a9.com/-/spec/opensearch/1.1/}',
		'vaext' : '{http://www.vizrt.com/atom-ext}',
		'vdf' : '{http://www.vizrt.com/types}',
		'ece' : '{http://www.escenic.com/2007/content-engine}',
		'playout' : '{http://ns.vizrt.com/ardome/playout}' }

logger = logging.getLogger()

def solrPrendiContentGiu( server,  sectionId, contentType, zuluDateFrom, zuluDateTo ):

	logger.debug('-------------- INIT ---- solrPrendiContent ----------- ' )

	dateFrom = zuluDateFrom.replace(':','%3A')
	dateTo = zuluDateTo.replace(':','%3A')
	listaContentId = []
	result = []


	try:

		auth = '%s:%s' % (os.environ['CUE_SOLR_USR'], os.environ['CUE_SOLR_PWD'])
		base64string = b64encode(auth.encode())
		base64string = base64string.decode("ascii")

		# prende items con 
		# state:published 
		# contenttype:contentType
		link_template = "http://internal.publishing.production.rsi.ch:8180/solr/collection1/select?q=*%3A*&fq=state%3Apublished&fq=section%3A__SECTION_ID__&fq=contenttype%3A" + contentType + "&fq=creationdate%3A+%5B+" + dateFrom + "+TO+" +  dateTo + "%5D" +"&start=__START__&rows=100&fl=id&wt=json&indent=true"
		# senza section
		link_template = "http://internal.publishing.staging.rsi.ch:8180/solr/collection1/select?q=*%3A*&fq=state%3Apublished&fq=contenttype%3A" + contentType + "&fq=creationdate%3A+%5B+" + dateFrom + "+TO+" +  dateTo + "%5D" +"&start=__START__&rows=100&fl=id,creationdate&wt=json&indent=true"
		link_template = server + "/select?q=*%3A*&fq=contenttype%3A" + contentType + "&fq=creationdate%3A+%5B+" + dateFrom + "+TO+" +  dateTo + "%5D" +"&start=__START__&rows=100&sort=creationdate+desc+&fl=id,creationdate,state,contenttype&wt=json&indent=true"
		# http://10.102.7.38:8180/solr/collection1/select?q=*%3A*&sort=id+desc&wt=json&indent=true

		# https://solr.cue-test.rsi.ch/solr/editorial/select?fl=objectid%2C%20contenttype%2Clastmodifieddate%2Ccreationdate%2Cpubdate_date&indent=true&q.op=OR&q=*%3A*&sort=id%20asc&wt=json
		link_template = server + "/select?q=*%3A*&fq=section%3A__SECTION_ID__&fq=contenttype%3A" + contentType + "&fq=creationdate%3A+%5B+" + dateFrom + "+TO+" +  dateTo + "%5D" +"&start=__START__&rows=100&sort=id+desc+&fl=objectid%2C%20contenttype%2Clastmodifieddate%2Ccreationdate%2Cpubdate_date&wt=json&indent=true"

		link = link_template.replace('__SECTION_ID__', sectionId).replace('__START__', '0')
		logger.debug( link )
		#logger.debug('link : ' + link )
		headers = { 'Authorization' : 'Basic %s' % base64string,
		'Content-Type': 'application/atom+xml'
		}

		request = urllib.request.Request(url=link, headers=headers, method='GET')
		with urllib.request.urlopen(request) as resultResponse:
			logger.debug ( resultResponse.status )
			logger.debug ( resultResponse.status )
			response = json.loads(resultResponse.read().decode('utf-8'))

		logger.debug('Presi dal solrPrendiContent : ' + str(response['response']['numFound']) + ' ' + "documents found")
		logger.debug('Presi dal solrPrendiContent : ' + str(response['response']['numFound']) + ' ' + "documents found") 

		#logger.debug(len(response['response']['docs']))

		listaContentId = response['response']['docs']
		logger.debug(len(listaContentId))

		totresult = int(response['response']['numFound'])
		items_per_page = int(100)

		if  totresult > items_per_page:
			#logger.debug(' giro sui next e prev ')
			# devi  girare sui next per prendere gli altri
			for x in range(int(float(totresult)/float(items_per_page))):
				__start__ = (x+1) * items_per_page
				logger.debug(str(x+1) + ' ' + str(__start__) + '/' + str(totresult))
				logger.debug(str(x+1) + ' ' + str(__start__)+ '/' + str(totresult) )

				#logger.debug(' giro per prenderli tutti')
				#e qui faccio la request sul campo next
				link_next = link_template.replace('__SECTION_ID__', sectionId).replace('__START__', str(__start__))
				#logger.debug(link_next)
				request = urllib.request.Request(url=link_next, headers=headers, method='GET')
				with urllib.request.urlopen(request) as resultResponse:
					logger.debug ( resultResponse.status )
					logger.debug ( resultResponse.status )
					response = json.loads(resultResponse.read().decode('utf-8'))

				listaContentId = listaContentId +  response['response']['docs']

				#listaContentId.append( response['response']['docs'] )
				#logger.debug(len(listaContentId))

		# per restituire tutti i campi
		result = listaContentId

		#for lis in listaContentId:
		# per passare da  {'id': 'article:13958752'}
		# a lista semplice di id 
		#result.append(lis.values()[0].split(':')[-1])

	except Exception as e:
		logger.warning ( 'PROBLEMI in solrPrendiContent : ' + str(e) )
		logger.debug( 'PROBLEMI in solrPrendiContent : ' + str(e)  )
		return []

	logger.debug( ' solrPrendiContent: content per section ' + sectionId + ' contenType = ' + contentType + ' from : ' + zuluDateFrom + ' to : ' + zuluDateTo + '  = % d ' % len(result) )
	logger.info( ' solrPrendiContent: content per section ' + sectionId + ' contenType = ' + contentType + ' from : ' + zuluDateFrom + ' to : ' + zuluDateTo + '  = % d ' % len(result))

	logger.debug('-------------- END ---- solrPrendiContent ----------- ' )
	return result


def solrPrendiPicturesFromTitle( server,  title, contentType, zuluDateFrom, zuluDateTo ):

	logger.debug('-------------- INIT ---- solrPrendiContent ----------- ' )
	sectionId = '1'
	dateFrom = zuluDateFrom.replace(':','%3A')
	dateTo = zuluDateTo.replace(':','%3A')
	listaContentId = []
	result = []


	try:

		auth = '%s:%s' % (os.environ['CUE_SOLR_USR'], os.environ['CUE_SOLR_PWD'])
		base64string = b64encode(auth.encode())
		base64string = base64string.decode("ascii")

		# prende items con 
		# state:published 
		# contenttype:contentType
		link_template = "http://internal.publishing.production.rsi.ch:8180/solr/collection1/select?q=*%3A*&fq=state%3Apublished&fq=section%3A__SECTION_ID__&fq=contenttype%3A" + contentType + "&fq=creationdate%3A+%5B+" + dateFrom + "+TO+" +  dateTo + "%5D" +"&start=__START__&rows=100&fl=id&wt=json&indent=true"
		# senza section
		link_template = "http://internal.publishing.staging.rsi.ch:8180/solr/collection1/select?q=*%3A*&fq=state%3Apublished&fq=contenttype%3A" + contentType + "&fq=creationdate%3A+%5B+" + dateFrom + "+TO+" +  dateTo + "%5D" +"&start=__START__&rows=100&fl=id,creationdate&wt=json&indent=true"
		link_template = server + "/select?q=*%3A*&fq=contenttype%3A" + contentType + "&fq=creationdate%3A+%5B+" + dateFrom + "+TO+" +  dateTo + "%5D" +"&start=__START__&rows=100&sort=creationdate+desc+&fl=id,creationdate,state,contenttype&wt=json&indent=true"

		# https://solr.cue-test.rsi.ch/solr/editorial/select?fl=objectid%2C%20contenttype%2Clastmodifieddate%2Ccreationdate%2Cpubdate_date&indent=true&q.op=OR&q=*%3A*&sort=id%20asc&wt=json
		link_template = server + "/select?q=*%3A*&fq=state%3Apublished&fq=title%3A" + title + "&fq=contenttype%3Apicture&start=__START__&rows=100&sort=id+asc+&fl=objectid%2C%20contenttype%2Clastmodifieddate%2Ccreationdate%2Cpubdate_date&wt=json&indent=true"
		link_template = server + "/select?fl=objectid&fq=contenttype%3Apicture&fq=title%3A" + title + "&indent=true&q.op=AND&q=*%3A*&sort=id%20asc&wt=json"

		link = link_template.replace('__SECTION_ID__', sectionId).replace('__START__', '0')
		logger.debug( link )
		#logger.debug('link : ' + link )
		headers = { 'Authorization' : 'Basic %s' % base64string,
		'Content-Type': 'application/atom+xml'
		}

		request = urllib.request.Request(url=link, headers=headers, method='GET')
		with urllib.request.urlopen(request) as resultResponse:
			logger.debug ( resultResponse.status )
			logger.debug ( resultResponse.status )
			response = json.loads(resultResponse.read().decode('utf-8'))

		logger.debug('Presi dal solrPrendiContent : ' + str(response['response']['numFound']) + ' ' + "documents found")
		logger.debug('Presi dal solrPrendiContent : ' + str(response['response']['numFound']) + ' ' + "documents found") 

		#logger.debug(len(response['response']['docs']))

		listaContentId = response['response']['docs']
		logger.debug(len(listaContentId))

		totresult = int(response['response']['numFound'])
		items_per_page = int(100)

		if  totresult > items_per_page:
			#logger.debug(' giro sui next e prev ')
			# devi  girare sui next per prendere gli altri
			for x in range(int(float(totresult)/float(items_per_page))):
				__start__ = (x+1) * items_per_page
				logger.debug(str(x+1) + ' ' + str(__start__) + '/' + str(totresult))
				logger.debug(str(x+1) + ' ' + str(__start__)+ '/' + str(totresult) )

				#logger.debug(' giro per prenderli tutti')
				#e qui faccio la request sul campo next
				link_next = link_template.replace('__SECTION_ID__', sectionId).replace('__START__', str(__start__))
				#logger.debug(link_next)
				request = urllib.request.Request(url=link_next, headers=headers, method='GET')
				with urllib.request.urlopen(request) as resultResponse:
					logger.debug ( resultResponse.status )
					logger.debug ( resultResponse.status )
					response = json.loads(resultResponse.read().decode('utf-8'))

				listaContentId = listaContentId +  response['response']['docs']

				#listaContentId.append( response['response']['docs'] )
				#logger.debug(len(listaContentId))

		# per restituire tutti i campi
		result = { title : listaContentId}
		logger.debug(result)

		#for lis in listaContentId:
		# per passare da  {'id': 'article:13958752'}
		# a lista semplice di id 
		#result.append(lis.values()[0].split(':')[-1])

	except Exception as e:
		logger.warning ( 'PROBLEMI in solrPrendiContent : ' + str(e) )
		logger.debug( 'PROBLEMI in solrPrendiContent : ' + str(e)  )
		return []

	logger.debug( ' solrPrendiContent: content per section ' + sectionId + ' contenType = ' + contentType + ' from : ' + zuluDateFrom + ' to : ' + zuluDateTo + '  = % d ' % len(result) )
	logger.info( ' solrPrendiContent: content per section ' + sectionId + ' contenType = ' + contentType + ' from : ' + zuluDateFrom + ' to : ' + zuluDateTo + '  = % d ' % len(result))

	logger.debug('-------------- END ---- solrPrendiContent ----------- ' )
	return result




def solrPrendiContentServer( server,  sectionId, contentType, zuluDateFrom, zuluDateTo ):

	logger.debug('-------------- INIT ---- solrPrendiContent ----------- ' )

	dateFrom = zuluDateFrom.replace(':','%3A')
	dateTo = zuluDateTo.replace(':','%3A')
	listaContentId = []
	result = []


	try:

		auth = '%s:%s' % (os.environ['CUE_SOLR_USR'], os.environ['CUE_SOLR_PWD'])
		base64string = b64encode(auth.encode())
		base64string = base64string.decode("ascii")

		# prende items con 
		# state:published 
		# contenttype:contentType
		link_template = "http://internal.publishing.production.rsi.ch:8180/solr/collection1/select?q=*%3A*&fq=state%3Apublished&fq=section%3A__SECTION_ID__&fq=contenttype%3A" + contentType + "&fq=creationdate%3A+%5B+" + dateFrom + "+TO+" +  dateTo + "%5D" +"&start=__START__&rows=100&fl=id&wt=json&indent=true"
		# senza section
		link_template = "http://internal.publishing.staging.rsi.ch:8180/solr/collection1/select?q=*%3A*&fq=state%3Apublished&fq=contenttype%3A" + contentType + "&fq=creationdate%3A+%5B+" + dateFrom + "+TO+" +  dateTo + "%5D" +"&start=__START__&rows=100&fl=id,creationdate&wt=json&indent=true"
		link_template = server + "/select?q=*%3A*&fq=contenttype%3A" + contentType + "&fq=creationdate%3A+%5B+" + dateFrom + "+TO+" +  dateTo + "%5D" +"&start=__START__&rows=100&sort=creationdate+desc+&fl=id,creationdate,state,contenttype&wt=json&indent=true"

		# https://solr.cue-test.rsi.ch/solr/editorial/select?fl=objectid%2C%20contenttype%2Clastmodifieddate%2Ccreationdate%2Cpubdate_date&indent=true&q.op=OR&q=*%3A*&sort=id%20asc&wt=json
		link_template = server + "/select?q=*%3A*&fq=state%3Apublished&fq=section%3A__SECTION_ID__&fq=contenttype%3A" + contentType + "&fq=pubdate_date%3A+%5B+" + dateFrom + "+TO+" +  dateTo + "%5D" +"&start=__START__&rows=100&sort=id+asc+&fl=objectid%2C%20contenttype%2Clastmodifieddate%2Ccreationdate%2Cpubdate_date&wt=json&indent=true"
		link_template = server + "/select?q=*%3A*&fq=state%3Apublished&fq=section%3A__SECTION_ID__&fq=contenttype%3A" + contentType + "&fq=creationdate%3A+%5B+" + dateFrom + "+TO+" +  dateTo + "%5D" +"&start=__START__&rows=100&sort=id+asc+&fl=objectid%2C%20contenttype%2Clastmodifieddate%2Ccreationdate%2Cpubdate_date&wt=json&indent=true"

		link = link_template.replace('__SECTION_ID__', sectionId).replace('__START__', '0')
		logger.debug( link )
		#logger.debug('link : ' + link )
		headers = { 'Authorization' : 'Basic %s' % base64string,
		'Content-Type': 'application/atom+xml'
		}

		request = urllib.request.Request(url=link, headers=headers, method='GET')
		with urllib.request.urlopen(request) as resultResponse:
			logger.debug ( resultResponse.status )
			logger.debug ( resultResponse.status )
			response = json.loads(resultResponse.read().decode('utf-8'))

		logger.debug('Presi dal solrPrendiContent : ' + str(response['response']['numFound']) + ' ' + "documents found")
		logger.debug('Presi dal solrPrendiContent : ' + str(response['response']['numFound']) + ' ' + "documents found") 

		#logger.debug(len(response['response']['docs']))

		listaContentId = response['response']['docs']
		logger.debug(len(listaContentId))

		totresult = int(response['response']['numFound'])
		items_per_page = int(100)

		if  totresult > items_per_page:
			#logger.debug(' giro sui next e prev ')
			# devi  girare sui next per prendere gli altri
			for x in range(int(float(totresult)/float(items_per_page))):
				__start__ = (x+1) * items_per_page
				logger.debug(str(x+1) + ' ' + str(__start__) + '/' + str(totresult))
				logger.debug(str(x+1) + ' ' + str(__start__)+ '/' + str(totresult) )

				#logger.debug(' giro per prenderli tutti')
				#e qui faccio la request sul campo next
				link_next = link_template.replace('__SECTION_ID__', sectionId).replace('__START__', str(__start__))
				#logger.debug(link_next)
				request = urllib.request.Request(url=link_next, headers=headers, method='GET')
				with urllib.request.urlopen(request) as resultResponse:
					logger.debug ( resultResponse.status )
					logger.debug ( resultResponse.status )
					response = json.loads(resultResponse.read().decode('utf-8'))

				listaContentId = listaContentId +  response['response']['docs']

				#listaContentId.append( response['response']['docs'] )
				#logger.debug(len(listaContentId))

		# per restituire tutti i campi
		result = listaContentId

		#for lis in listaContentId:
		# per passare da  {'id': 'article:13958752'}
		# a lista semplice di id 
		#result.append(lis.values()[0].split(':')[-1])

	except Exception as e:
		logger.warning ( 'PROBLEMI in solrPrendiContent : ' + str(e) )
		logger.debug( 'PROBLEMI in solrPrendiContent : ' + str(e)  )
		return []

	logger.debug( ' solrPrendiContent: content per section ' + sectionId + ' contenType = ' + contentType + ' from : ' + zuluDateFrom + ' to : ' + zuluDateTo + '  = % d ' % len(result) )
	logger.info( ' solrPrendiContent: content per section ' + sectionId + ' contenType = ' + contentType + ' from : ' + zuluDateFrom + ' to : ' + zuluDateTo + '  = % d ' % len(result))

	logger.debug('-------------- END ---- solrPrendiContent ----------- ' )
	return result

def solrPrendiContent( sectionId, contentType, zuluDateFrom, zuluDateTo ):

	logger.debug('-------------- INIT ---- solrPrendiContent ----------- ' )

	dateFrom = zuluDateFrom.replace(':','%3A')
	dateTo = zuluDateTo.replace(':','%3A')
	listaContentId = []
	result = []


	try:

		auth = '%s:%s' % (os.environ['CUE_SOLR_USR'], os.environ['CUE_SOLR_PWD'])
		base64string = b64encode(auth.encode())
		base64string = base64string.decode("ascii")

		# prende items con 
		# state:published 
		# contenttype:contentType
		link_template = "http://internal.publishing.production.rsi.ch:8180/solr/collection1/select?q=*%3A*&fq=state%3Apublished&fq=section%3A__SECTION_ID__&fq=contenttype%3A" + contentType + "&fq=creationdate%3A+%5B+" + dateFrom + "+TO+" +  dateTo + "%5D" +"&start=__START__&rows=100&fl=id&wt=json&indent=true"
		# senza section
		link_template = "http://internal.publishing.staging.rsi.ch:8180/solr/collection1/select?q=*%3A*&fq=state%3Apublished&fq=contenttype%3A" + contentType + "&fq=creationdate%3A+%5B+" + dateFrom + "+TO+" +  dateTo + "%5D" +"&start=__START__&rows=100&fl=id,creationdate&wt=json&indent=true"
		link_template = os.environ['SOLR_SERVER'] + "/select?q=*%3A*&fq=publication%3A%22rsi%22&fq=contenttype%3A" + contentType + "&fq=creationdate%3A+%5B+" + dateFrom + "+TO+" +  dateTo + "%5D" +"&start=__START__&rows=100&fl=id,creationdate,state,contenttype&wt=json&indent=true"
		# prende solo published
		link_template = os.environ['SOLR_SERVER'] + "/select?q=*%3A*&fq=publication%3A%22rsi%22&fq=state%3A(published+OR+draft-published)&fq=section%3A__SECTION_ID__&fq=contenttype%3A" + contentType + "&fq=pubdate_date%3A+%5B+" + dateFrom + "+TO+" +  dateTo + "%5D" +"&start=__START__&rows=100&sort=pubdate_date+desc+&fl=id,objectid,pubdate_date,state,contenttype,lastmodifieddate&wt=json&indent=true"

		link = link_template.replace('__SECTION_ID__', sectionId).replace('__START__', '0')
		logger.debug( link )
		#logger.debug('link : ' + link )
		headers = { 'Authorization' : 'Basic %s' % base64string,
		'Content-Type': 'application/atom+xml'
		}

		request = urllib.request.Request(url=link, headers=headers, method='GET')
		with urllib.request.urlopen(request) as resultResponse:
			logger.debug ( resultResponse.status )
			logger.debug ( resultResponse.status )
			response = json.loads(resultResponse.read().decode('utf-8'))

		logger.debug('Presi dal solrPrendiContent : ' + str(response['response']['numFound']) + ' ' + "documents found")
		logger.debug('Presi dal solrPrendiContent : ' + str(response['response']['numFound']) + ' ' + "documents found") 

		#logger.debug(len(response['response']['docs']))

		listaContentId = response['response']['docs']
		logger.debug(len(listaContentId))

		totresult = int(response['response']['numFound'])
		items_per_page = int(100)

		if  totresult > items_per_page:
			#logger.debug(' giro sui next e prev ')
			# devi  girare sui next per prendere gli altri
			for x in range(int(float(totresult)/float(items_per_page))):
				__start__ = (x+1) * items_per_page
				logger.debug(str(x+1) + ' ' + str(__start__) + ' / ' + str(totresult) )
				logger.debug(str(x+1) + ' ' + str(__start__)  + ' / ' + str(totresult) )

				#logger.debug(' giro per prenderli tutti')
				#e qui faccio la request sul campo next
				link_next = link_template.replace('__SECTION_ID__', sectionId).replace('__START__', str(__start__))
				#logger.debug(link_next)
				request = urllib.request.Request(url=link_next, headers=headers, method='GET')
				with urllib.request.urlopen(request) as resultResponse:
					logger.debug ( resultResponse.status )
					logger.debug ( resultResponse.status )
					response = json.loads(resultResponse.read().decode('utf-8'))

				listaContentId = listaContentId +  response['response']['docs']

				#listaContentId.append( response['response']['docs'] )
				#logger.debug(len(listaContentId))

		result = listaContentId


	except Exception as e:
		logger.warning ( 'PROBLEMI in solrPrendiContent : ' + str(e) )
		logger.debug( 'PROBLEMI in solrPrendiContent : ' + str(e)  )
		return []

	logger.debug( ' solrPrendiContent: content per section ' + sectionId + ' contenType = ' + contentType + ' from : ' + zuluDateFrom + ' to : ' + zuluDateTo + '  = % d ' % len(result) )
	logger.info( ' solrPrendiContent: content per section ' + sectionId + ' contenType = ' + contentType + ' from : ' + zuluDateFrom + ' TO ' + zuluDateTo + '  = % d ' % len(result))

	logger.debug('-------------- END ---- solrPrendiContent ----------- ' )
	return result



def solrPrendiContentDeleted( sectionId, contentType, zuluDateFrom, zuluDateTo ):

	logger.debug('-------------- INIT ---- solrPrendiContent ----------- ' )

	dateFrom = zuluDateFrom.replace(':','%3A')
	dateTo = zuluDateTo.replace(':','%3A')
	dateTo = 'NOW'
	listaContentId = []
	result = []


	try:

		auth = '%s:%s' % (os.environ['ECE_USER'], os.environ['ECE_PWD'])
		base64string = b64encode(auth.encode())
		base64string = base64string.decode("ascii")

		# prende items con 
		# state:published 
		# contenttype:contentType
		link_template = "http://internal.publishing.production.rsi.ch:8180/solr/collection1/select?q=*%3A*&fq=state%3Apublished&fq=section%3A__SECTION_ID__&fq=contenttype%3A" + contentType + "&fq=creationdate%3A+%5B+" + dateFrom + "+TO+" +  dateTo + "%5D" +"&start=__START__&rows=100&fl=id&wt=json&indent=true"
		# senza section
		link_template = "http://internal.publishing.staging.rsi.ch:8180/solr/collection1/select?q=*%3A*&fq=state%3Apublished&fq=contenttype%3A" + contentType + "&fq=creationdate%3A+%5B+" + dateFrom + "+TO+" +  dateTo + "%5D" +"&start=__START__&rows=100&fl=id,creationdate&wt=json&indent=true"
		link_template = os.environ['SOLR_SERVER'] + "/select?q=*%3A*&fq=publication%3A%22rsi%22&fq=contenttype%3A" + contentType + "&fq=creationdate%3A+%5B+" + dateFrom + "+TO+" +  dateTo + "%5D" +"&start=__START__&rows=100&fl=id,creationdate,state,contenttype&wt=json&indent=true"
		# prende solo published
		# http://10.102.7.38:8180/solr/collection1/select?q=*%3A*&fq=-state%3A(published+OR+draft-published)&fq=publication%3Arsi&fq=-contenttype%3Acom.escenic.section&fl=objectid%2Ccontenttype%2Cstate%2Ctitle%2Ccreationdate%2Clastmodifieddate%2Chome_section&wt=json&indent=true
		link_template = os.environ['SOLR_SERVER'] + "/select?q=*%3A*&fq=publication%3A%22rsi%22&fq=-state%3A(published+OR+draft-published)&fq=-contenttype%3Acom.escenic.section&start=__START__&rows=100&sort=creationdate+desc+&fl=objectid%2Ccontenttype%2Cstate%2Ctitle%2Ccreationdate%2Clastmodifieddate%2Chome_section&wt=json&indent=true"

		link = link_template.replace('__SECTION_ID__', sectionId).replace('__START__', '0')
		logger.debug( link )
		#logger.debug('link : ' + link )
		headers = { 'Authorization' : 'Basic %s' % base64string,
		'Content-Type': 'application/atom+xml'
		}

		request = urllib.request.Request(url=link, headers=headers, method='GET')
		with urllib.request.urlopen(request) as resultResponse:
			logger.debug ( resultResponse.status )
			logger.debug ( resultResponse.status )
			response = json.loads(resultResponse.read().decode('utf-8'))

		logger.debug('Presi dal solrPrendiContent : ' + str(response['response']['numFound']) + ' ' + "documents found")
		logger.debug('Presi dal solrPrendiContent : ' + str(response['response']['numFound']) + ' ' + "documents found") 

		#logger.debug(len(response['response']['docs']))

		listaContentId = response['response']['docs']
		logger.debug(len(listaContentId))

		totresult = int(response['response']['numFound'])
		items_per_page = int(100)

		if  totresult > items_per_page:
			#logger.debug(' giro sui next e prev ')
			# devi  girare sui next per prendere gli altri
			for x in range(int(float(totresult)/float(items_per_page))):
				__start__ = (x+1) * items_per_page
				logger.debug(str(x+1) + ' ' + str(__start__) )
				logger.debug(str(x+1) + ' ' + str(__start__) )

				#logger.debug(' giro per prenderli tutti')
				#e qui faccio la request sul campo next
				link_next = link_template.replace('__SECTION_ID__', sectionId).replace('__START__', str(__start__))
				#logger.debug(link_next)
				request = urllib.request.Request(url=link_next, headers=headers, method='GET')
				with urllib.request.urlopen(request) as resultResponse:
					logger.debug ( resultResponse.status )
					logger.debug ( resultResponse.status )
					response = json.loads(resultResponse.read().decode('utf-8'))

				listaContentId = listaContentId +  response['response']['docs']

				#listaContentId.append( response['response']['docs'] )
				#logger.debug(len(listaContentId))

		# per restituire tutti i campi
		# result = listaContentId
		# GESTIONE BLACKLIST
		for lis in listaContentId:
			result.append(lis)


	except Exception as e:
		logger.warning ( 'PROBLEMI in solrPrendiContent : ' + str(e) )
		logger.debug( 'PROBLEMI in solrPrendiContent : ' + str(e)  )
		return []

	logger.debug( ' solrPrendiContent: content per section ' + sectionId + ' contenType = ' + contentType + ' from : ' + zuluDateFrom + ' to : ' + zuluDateTo + '  = % d ' % len(result) )
	logger.info( ' solrPrendiContent: content per section ' + sectionId + ' contenType = ' + contentType + ' from : ' + zuluDateFrom + ' to : ' + zuluDateTo + '  = % d ' % len(result))

	logger.debug('-------------- END ---- solrPrendiContent ----------- ' )
	return result



def solrCountContent( sectionId, contentType, zuluDateFrom, zuluDateTo ):

	logger.debug('-------------- INIT ---- solrCountContent ----------- ' )

	dateFrom = zuluDateFrom.replace(':','%3A')
	dateTo = zuluDateTo.replace(':','%3A')
	listaContentId = []
	result = []
	totresult = 0


	try:

		auth = '%s:%s' % (os.environ['ECE_USER'], os.environ['ECE_PWD'])
		base64string = b64encode(auth.encode())
		base64string = base64string.decode("ascii")

		# prende items con 
		# state:published 
		# contenttype:contentType
		link_template = "http://internal.publishing.production.rsi.ch:8180/solr/collection1/select?q=*%3A*&fq=state%3Apublished&fq=section%3A__SECTION_ID__&fq=contenttype%3A" + contentType + "&fq=creationdate%3A+%5B+" + dateFrom + "+TO+" +  dateTo + "%5D" +"&start=__START__&rows=100&fl=id&wt=json&indent=true"
		# senza section
		link_template = "http://internal.publishing.staging.rsi.ch:8180/solr/collection1/select?q=*%3A*&fq=state%3Apublished&fq=contenttype%3A" + contentType + "&fq=creationdate%3A+%5B+" + dateFrom + "+TO+" +  dateTo + "%5D" +"&start=__START__&rows=100&fl=id,creationdate&wt=json&indent=true"
		link_template = os.environ['SOLR_SERVER'] + "/select?q=*%3A*&fq=publication%3A%22rsi%22&fq=contenttype%3A" + contentType + "&fq=creationdate%3A+%5B+" + dateFrom + "+TO+" +  dateTo + "%5D" +"&start=__START__&rows=100&fl=id,creationdate,state,contenttype&wt=json&indent=true"
		link_template = os.environ['SOLR_SERVER'] + "/select?q=*%3A*&fq=publication%3A%22rsi%22&fq=contenttype%3A" + contentType + "&fq=section%3A__SECTION_ID__&fq=creationdate%3A+%5B+" + dateFrom + "+TO+" +  dateTo + "%5D" +"&start=__START__&rows=100&fl=id,creationdate,state,contenttype&wt=json&indent=true"
		link_template = os.environ['SOLR_SERVER'] + "/select?q=*%3A*&fq=publication%3A%22rsi%22&fq=state%3Apublished&fq=contenttype%3A" + contentType + "&fq=section%3A__SECTION_ID__&fq=creationdate%3A+%5B+" + dateFrom + "+TO+" +  dateTo + "%5D" +"&start=__START__&rows=100&fl=id,creationdate,state,contenttype&wt=json&indent=true"

		link = link_template.replace('__SECTION_ID__', sectionId).replace('__START__', '0')
		logger.debug( link )
		#logger.debug('link : ' + link )
		headers = { 'Authorization' : 'Basic %s' % base64string,
		'Content-Type': 'application/atom+xml'
		}

		request = urllib.request.Request(url=link, headers=headers, method='GET')
		with urllib.request.urlopen(request) as resultResponse:
			logger.debug ( resultResponse.status )
			logger.debug ( resultResponse.status )
			response = json.loads(resultResponse.read().decode('utf-8'))

		logger.debug('Presi dal solrCountContent : ' + str(response['response']['numFound']) + ' ' + "documents found")
		logger.debug('Presi dal solrCountContent : ' + str(response['response']['numFound']) + ' ' + "documents found") 

		#logger.debug(len(response['response']['docs']))

		listaContentId = response['response']['docs']
		logger.debug(len(listaContentId))

		totresult = int(response['response']['numFound'])

	except Exception as e:
		logger.warning ( 'PROBLEMI in solrCountContent : ' + str(e) )
		logger.debug( 'PROBLEMI in solrCountContent : ' + str(e)  )
		return []

	logger.debug( ' solrCountContent: content per section ' + sectionId + ' contenType = ' + contentType + ' from : ' + zuluDateFrom + ' to : ' + zuluDateTo + '  = % d ' % len(result) )
	logger.info( ' solrCountContent: content per section ' + sectionId + ' contenType = ' + contentType + ' from : ' + zuluDateFrom + ' to : ' + zuluDateTo + '  = % d ' % len(result))

	logger.debug('-------------- END ---- solrCountContent ----------- ' )
	return totresult

def solrPrendiSections( zuluDateFrom, zuluDateTo ):

	logger.debug('-------------- INIT ---- solrPrendiSections ----------- ' )

	dateFrom = zuluDateFrom.replace(':','%3A')
	dateTo = zuluDateTo.replace(':','%3A')
	listaContentId = []
	result = []


	try:

		auth = '%s:%s' % (os.environ['ECE_USER'], os.environ['ECE_PWD'])
		base64string = b64encode(auth.encode())
		base64string = base64string.decode("ascii")

		# prende items con 
		# state:published 
		# contenttype:contentType
		# prende published e draft-published
		link_template = os.environ['SOLR_SERVER'] + "/select?q=*%3A*&fq=publication%3A%22rsi%22&fq=state%3A(published+OR+draft-published)&fq=contenttype%3Acom.escenic.section&fq=creationdate%3A+%5B+" + dateFrom + "+TO+" +  dateTo + "%5D" +"&start=__START__&rows=100&sort=creationdate+desc+&fl=id,creationdate,state,contenttype&wt=json&indent=true"

		link = link_template.replace('__START__', '0')
		logger.debug( link )
		#logger.debug('link : ' + link )
		headers = { 'Authorization' : 'Basic %s' % base64string,
		'Content-Type': 'application/atom+xml'
		}

		request = urllib.request.Request(url=link, headers=headers, method='GET')
		with urllib.request.urlopen(request) as resultResponse:
			logger.debug ( resultResponse.status )
			logger.debug ( resultResponse.status )
			response = json.loads(resultResponse.read().decode('utf-8'))

		logger.debug('Presi dal solrPrendiSections : ' + str(response['response']['numFound']) + ' ' + "documents found")
		logger.debug('Presi dal solrPrendiSections : ' + str(response['response']['numFound']) + ' ' + "documents found") 

		#logger.debug(len(response['response']['docs']))

		listaContentId = response['response']['docs']
		logger.debug(len(listaContentId))

		totresult = int(response['response']['numFound'])
		items_per_page = int(100)

		if  totresult > items_per_page:
			#logger.debug(' giro sui next e prev ')
			# devi  girare sui next per prendere gli altri
			for x in range(int(float(totresult)/float(items_per_page))):
				__start__ = (x+1) * items_per_page
				logger.debug(str(x+1) + ' ' + str(__start__) + ' / ' + str(totresult) )
				logger.debug(str(x+1) + ' ' + str(__start__)  + ' / ' + str(totresult) )

				#logger.debug(' giro per prenderli tutti')
				#e qui faccio la request sul campo next
				link_next = link_template.replace('__START__', str(__start__))
				#logger.debug(link_next)
				request = urllib.request.Request(url=link_next, headers=headers, method='GET')
				with urllib.request.urlopen(request) as resultResponse:
					logger.debug ( resultResponse.status )
					logger.debug ( resultResponse.status )
					response = json.loads(resultResponse.read().decode('utf-8'))

				listaContentId = listaContentId +  response['response']['docs']

				#listaContentId.append( response['response']['docs'] )
				#logger.debug(len(listaContentId))

		# per restituire tutti i campi
		# result = listaContentId
		# GESTIONE BLACKLIST
		for lis in listaContentId:
		# per passare da  {'id': 'article:13958752'}
		# a lista semplice di id 
		# e verificare la BlackList
			value = lis['id'].split(':')[-1]
			if not ( value in Blist.lista ) :
				result.append(lis['id'].split(':')[-1])
			else:
				logger.debug( ' trovato id : ' + value + ' in Blist -> lo tolgo ' )
		# GESTIONE BLACKLIST


	except Exception as e:
		logger.warning ( 'PROBLEMI in solrPrendiSections : ' + str(e) )
		logger.debug( 'PROBLEMI in solrPrendiSections : ' + str(e)  )
		return []

	logger.debug( ' solrPrendiSections: sections from : ' + zuluDateFrom + ' to : ' + zuluDateTo + '  = % d ' % len(result) )
	logger.info( ' solrPrendiSections: sections from : ' + zuluDateFrom + ' to : ' + zuluDateTo + '  = % d ' % len(result))

	logger.debug('-------------- END ---- solrPrendiSections ----------- ' )
	return result




if __name__ == "__main__":

	os.environ['ECE_USER'] = 'TSMM'
	os.environ['ECE_PWD'] = '8AKjwWXiWAFTxb2UM3pZ'
	
	# per tesare cue
	os.environ['ECE_USER'] = 'rsisolr'
	os.environ['ECE_PWD'] = '6igq-YOYOE1C27ftpnTPHrfJgh8FewND'
	os.environ['CUE_SOLR_USR'] = 'rsisolr'
	os.environ['CUE_SOLR_PWD'] = '6igq-YOYOE1C27ftpnTPHrfJgh8FewND'

	#lista = solrPrendiContentServer('https://solr.cue.rsi.ch/solr/editorial', '1', 'event', '2017-09-01T00:00:00Z',  '2017-12-01T00:00:00Z')
	lista = solrPrendiContentServer('https://solr.cue.rsi.ch/solr/editorial', '1', 'story', '2017-09-01T00:00:00Z',  '2023-12-01T00:00:00Z')
	logger.debug(lista)

	exit(0)
	os.environ['ECE_MODEL'] = 'http://internal.publishing.staging.rsi.ch/webservice/publication/rsi/escenic/model/'
	os.environ['IMG_CREATE_URL'] = 'http://internal.publishing.staging.rsi.ch/webservice/escenic/section/__CREATE_SECTION__/content-items'
	os.environ['ECE_SERVER'] = 'http://internal.publishing.staging.rsi.ch/webservice/escenic/content/'
	os.environ['ECE_SECTION'] = 'http://internal.publishing.staging.rsi.ch/webservice/escenic/section/'
	os.environ['ECE_BRAND'] = 'http://internal.publishing.staging.rsi.ch/webservice-extensions/srg/sectionIdForBrand/?publicationName=rsi&channel=__CHANNEL__&brand=__BRAND__'

	os.environ['CREATE_URL'] =  "http://internal.publishing.staging.rsi.ch/webservice/escenic/section/__CREATE_SECTION__/content-items"
	os.environ['UPDATE_FILE'] =  "/home/perucccl/Webservices/STAGING/newMamServices/Resources/_cambiamento_"
	os.environ['SOLR_SERVER'] = "http://internal.publishing.staging.rsi.ch:8180/solr/collection1"
	os.environ['SOLR_SERVER'] = "http://internal.publishing.production.rsi.ch:8180/solr/collection1"
	
	Environment_Variables = {'COUCH_DB' : 'testnuovo', 'COUCH_HOST' : 'rsis-zp-mongo1', 'COUCH_PORT':'5984', 'COUCH_USER':'admin', 'COUCH_PWD':'78-AjhQ','IMPORT_SECTION': '9736','CREATE_URL':'http://internal.publishing.staging.rsi.ch/webservice/escenic/section/__CREATE_SECTION__/content-items','IMG_CREATE_URL':'http://internal.publishing.staging.rsi.ch/webservice/escenic/section/__CREATE_SECTION__/content-items', 'VID_RESOURCE_TEMPLATE':'/home/perucccl/Webservices/STAGING/CreateTranscodable/Resources/template_pVideo.xml.stag', 'IMG_RESOURCE_TEMPLATE':'/home/perucccl/Webservices/STAGING/newMamServices/Resources/template_picture.xml','LOCK_URL' : 'http://internal.publishing.production.rsi.ch/webservice/escenic/lock/article/','LOCK_NAME' : 'template_lock.xml','LOCK_ID' : '11868353' ,'REST_POST_URL': 'http://publishing.staging.rsi.ch/rsi-api/intlay/mockup/importkeyframe/keyframes.json','REST_GET_URL': 'http://publishing.staging.rsi.ch/rsi-api/intlay/mockup/importkeyframe/keyframes.json', 'FTP_ARCHIVE_DIR' : '/mnt/rsi_import/keyframe_traffic/archived/',  'FTP_DIR' : '/mnt/rsi_import/keyframe_traffic/test/','VERSION' : '3.2','ECE_USER' : 'TSMM', 'ECE_PWD':'8AKjwWXiWAFTxb2UM3pZ', 'ECE_MODEL':'http://internal.publishing.staging.rsi.ch/webservice/publication/rsi/escenic/model/','ECE_SERVER' : 'http://internal.publishing.staging.rsi.ch/webservice/escenic/content/','ECE_BINARY' : 'http://internal.publishing.staging.rsi.ch/webservice/escenic/binary','ECE_BRAND' : 'http://internal.publishing.staging.rsi.ch/webservice-extensions/srg/sectionIdForBrand/?publicationName=rsi&channel=__CHANNEL__&brand=__BRAND__','ECE_THUMB' : 'http://internal.publishing.staging.rsi.ch/webservice/thumbnail/article/', 'ECE_SECTION' : 'http://internal.publishing.staging.rsi.ch/webservice/escenic/section/', 'UPDATE_FILE' : '/home/perucccl/Webservices/STAGING/newMamServices/Resources/_cambiamento_','ARCHIVE_NAME' : '/home/perucccl/STAGING/APICoreX/Resources/_LivestreamingArchive_','LOCK_RESOURCE_DIR':'/home/perucccl/Webservices/STAGING/newMamServices/Resources/','RESOURCE_DIR':'/home/perucccl/Webservices/STAGING/newMamServices/Resources/','DB_NAME' : '/home/perucccl/Webservices/STAGING/CreateTranscodable/Resources/_ImportKeyFramesDb_', 'http_proxy': 'http://gateway.zscloud.net:10268', 'LESSOPEN': '||/usr/bin/lesspipe.sh %s', 'SSH_CLIENT': '146.159.126.207 57239 22', 'SELINUX_USE_CUR RENT_RANGE': '', 'LOGNAME': 'perucccl', 'USER': 'perucccl', 'HOME': '/home/perucccl', 'PATH': '/usr/local/bin:/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/sbin:/home/perucccl/bin', 'LANG': 'en_US.UTF-8', 'TERM': 'xterm', 'SHELL': '/bin/bash', 'SHLVL': '1', 'G_BROKEN_FILENAME S': '1', 'HISTSIZE': '1000', 'https_proxy': 'http://gateway.zscloud.net:10268', 'SELINUX_ROLE_REQUESTED': '', '_': '/usr/bin/python', 'SSH_CONNECTION': '146.159.126.207 57239 10.72.112.35 22', 'SSH_TTY': '/dev/pts/1', 'HOSTNAME': 'rsis-prod-web1.media.int', 'SELINUX_LEVE L_REQUESTED': '', 'HISTCONTROL': 'ignoredups', 'no_proxy': 'amazonaws.com,rsis-zp-mongo1,localhost,127.0.0.1,.media.int,rsis-tifone-t1,rsis-tifone-t2,rsis-tifone-t,.rsi.ch,10.102.7.38:8180,10.101.8.27:8180,.twitter.com', 'MAIL': '/var/spool/mail/perucccl', 'LS_COLORS': 'rs=0:di=01;34:ln=01;36:mh=00: pi=40;33:so=01;35:do=01;35:bd=40;33;01:cd=40;33;01:or=40;31;01:mi=01;05;37;41:su=37;41:sg=30;43:ca=30;41:tw=30;42:ow=34;42:st=37;44:ex=01;32:*.tar=01;31:*.tgz=01;31:*.arj=01;31:*.taz=01;31:*.lzh=01;31:*.lzma=01;31:*.tlz=01;31:*.txz=01;31:*.zip=01;31:*.z=01;31:*.Z=01;31:* .dz=01;31:*.gz=01;31:*.lz=01;31:*.xz=01;31:*.bz2=01;31:*.tbz=01;31:*.tbz2=01;31:*.bz=01;31:*.tz=01;31:*.deb=01;31:*.rpm=01;31:*.jar=01;31:*.rar=01;31:*.ace=01;31:*.zoo=01;31:*.cpio=01;31:*.7z=01;31:*.rz=01;31:*.jpg=01;35:*.jpeg=01;35:*.gif=01;35:*.bmp=01;35:*.pbm=01;35:* .pgm=01;35:*.ppm=01;35:*.tga=01;35:*.xbm=01;35:*.xpm=01;35:*.tif=01;35:*.tiff=01;35:*.png=01;35:*.svg=01;35:*.svgz=01;35:*.mng=01;35:*.pcx=01;35:*.mov=01;35:*.mpg=01;35:*.mpeg=01;35:*.m2v=01;35:*.mkv=01;35:*.ogm=01;35:*.mp4=01;35:*.m4v=01;35:*.mp4v=01;35:*.vob=01;35:*.qt =01;35:*.nuv=01;35:*.wmv=01;35:*.asf=01;35:*.rm=01;35:*.rmvb=01;35:*.flc=01;35:*.avi=01;35:*.fli=01;35:*.flv=01;35:*.gl=01;35:*.dl=01;35:*.xcf=01;35:*.xwd=01;35:*.yuv=01;35:*.cgm=01;35:*.emf=01;35:*.axv=01;35:*.anx=01;35:*.ogv=01;35:*.ogx=01;35:*.aac=01;36:*.au=01;36:*.f lac=01;36:*.mid=01;36:*.midi=01;36:*.mka=01;36:*.mp3=01;36:*.mpc=01;36:*.ogg=01;36:*.ra=01;36:*.wav=01;36:*.axa=01;36:*.oga=01;36:*.spx=01;36:*.xspf=01;36:'} 
	for param in Environment_Variables.keys():
		os.environ[param] = Environment_Variables[ param ]

	lista = solrPrendiSections('2022-10-13T00:00:00Z',  'NOW')
	# 2022-12-19 18:33:00.861
	lista = solrPrendiSections('2022-12-19T18:34:00Z',  'NOW')
	logger.debug(lista)
	exit(0)
	lista = solrPrendiContentDeleted('4', 'mamProgrammeVideo', '2000-04-26T00:00:00Z',  'NOW')
	exit(0)

	listaVideo = ['programmeVideo','transcodableVideo','vmeVideo','migrationVideo', 'programmeAudio','transcodableAudio','vmeAudio','migrationAudio']

	listaDaFare = []

	for lis in listaVideo:
		#num = solrCountContent('5', lis, '2006-01-01T00:00:00Z',  '2022-08-31T23:59:59Z')
		#logger.debug(lis + ' con -> ' + str(num))
		lista = solrPrendiContent('5', lis, '2006-01-01T00:00:00Z',  '2022-08-31T23:59:59Z')
		logger.debug(lis + ' con -> ' + str(len(lista)))
		listaDaFare += lista

	logger.debug(str(len(listaDaFAre)))
	
	with open('listaDaFare.txt', 'w') as filehandle:
	    json.dump(listaDaFare, filehandle)

	exit(0)


	#lista = solrPrendiContent('4', 'mamProgramme', '2021-04-03T00%3A00%3A00Z')
	lista = solrPrendiContent('4', 'mamProgramme', '2021-04-26T00:00:00Z',  '2021-04-27T00:00:00Z')
	lista = solrPrendiContent('4', 'mamProgrammeVideo', '2021-04-26T00:00:00Z',  '2021-04-27T00:00:00Z')
	
	'''
	with open('listid.txt', 'w') as filehandle:
	    json.dump(lista, filehandle)
	exit(0)
	

	with open('listid.txt', 'r') as filehandle:
	    basicList = json.load(filehandle)
	
	for lis in basicList:

		logger.debug( (lis['id'].split('article:')[-1])) )
		deleteId(lis['id'].split('article:')[-1])
	'''
	exit(0)


	
