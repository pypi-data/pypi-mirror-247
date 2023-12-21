import logging
import xml.etree.ElementTree
import xml.etree.ElementTree as ET
import os
import json
import re
from datetime import datetime

import rsi_python_lib.pyTools as pyTools

# definizione dei namespaces per parsaqre gli atom
namespaces = { 'atom':'{http://www.w3.org/2005/Atom}',
		'dcterms' : '{http://purl.org/dc/terms/}',
		'mam' : '{http://www.vizrt.com/2010/mam}',
		'age' : '{http://purl.org/atompub/age/1.0}',
		'opensearch' : '{http://a9.com/-/spec/opensearch/1.1/}',
		'vaext' : '{http://www.vizrt.com/atom-ext}',
		'app' : '{http://www.w3.org/2007/app}',
		'vdf' : '{http://www.vizrt.com/types}',
		'metadata' : '{http://xmlns.escenic.com/2010/atom-metadata}',
		'thr' : '{http://purl.org/syndication/thread/1.0}',
		'xmlns' : '{http://www.sitemaps.org/schemas/sitemap/0.9}',
		#'': '{http://www.w3.org/1999/xhtml}',
		'playout' : '{http://ns.vizrt.com/ardome/playout}' }

logger = logging.getLogger()

class xmlSitemapIndexParser(object):

	def __init__(self, contentXml):
		if contentXml is None:
			# ne voglio creare una nuova
			# quindi parto con contentXml =  
			contentXml = '<?xml version="1.0" encoding="UTF-8"?> <sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"> </sitemapindex>'
		if isinstance( contentXml, (bytes) ):
			self.contentXml = contentXml.decode("utf-8") 
		else:
			self.contentXml = contentXml
		try:
			root = ET.fromstring(self.contentXml)
			self.root = root
			logger.debug(self.root.tag)
			self.lista_sitemaps = None
			# questa e la lista delle url presenti nella map
			self.lista_sitemaps = self.root.findall( namespaces['xmlns'] + "sitemap" )
			logger.debug(self.lista_sitemaps)
			self.dumpDoc()
			
		except Exception as e:
			logger.error( 'Error in __genRoot : ' + str(e) )
			return 

	def getRoot(self):
		return self.root

	def getXml(self):
		return self.contentXml

	def dumpDoc(self):
		#tree = ET.ElementTree(self.root)
		#ET.dump(tree)
		logger.debug(ET.tostring(self.root, encoding='unicode'))
	
	def getDocXml(self):
		return ET.tostring(self.root, encoding='unicode')

	def writeToFile( self, filename):
		tree=ET.ElementTree(self.root) 
		tree.write(filename, xml_declaration=True, method='xml')

	def aggiungi_crea_elem( self, value ):
		#logger.debug('---------------- INIT aggiungi_crea_elem --------------------')
		#logger.debug('---------------- INIT aggiungi_crea_elem --------------------')
		# creo element da aggiungere
		__elem = ET.Element( "sitemap" )
		__loc = ET.SubElement( __elem, "loc")
		__loc.text = value

		self.root.append( __elem )

		#self.dumpDoc()
		#logger.debug('---------------- END aggiungi_crea_elem --------------------')
		#logger.debug('---------------- END aggiungi_crea_elem --------------------')





class xmlSitemapParser(object):

	def __init__(self, contentXml):
		if isinstance( contentXml, (bytes) ):
			self.contentXml = contentXml.decode("utf-8") 
		else:
			self.contentXml = contentXml
		try:
			root = ET.fromstring(self.contentXml)
			self.root = root
			logger.debug(self.root.tag)
			self.lista_urls = None
			# questa e la lista delle url presenti nella map
			self.lista_urls = self.root.findall( namespaces['xmlns'] + "url" )
			# questa e' a lista degli ID presenti nella map
			self.lista_ids = []
			self.crea_lista_ids()

			self.dict_id_elem = {}
			# e questo e' un dizionario nella forma  :
			#{704775: <Element '{http://www.sitemaps.org/schemas/sitemap/0.9}url' at 0x7f548ebe7c28>, 
			# 704776: <Element '{http://www.sitemaps.org/schemas/sitemap/0.9}url' at 0x7f548ec192c8>, 
			# 704939: <Element '{http://www.sitemaps.org/schemas/sitemap/0.9}url' at 0x7f548ec19408>}
			# comodo per ordinare le entry

			self.dict_id_lastmod = {}
			# questa e la lista delle lastmod in int presenti nella map
			# e questo e' un dizionario nella forma  :
			#{ 704775: 1695938709000 ,
			# 704776: 1695961204000 ,
			# 704939: 1695973254000}
			# comodo per capire quelli che devono andare in archivio
			self.crea_dict_all()
			
			
		except Exception as e:
			logger.error( 'Error in __genRoot : ' + str(e) )
			return 

	def getRoot(self):
		return self.root

	def getXml(self):
		return self.contentXml

	def get_lista_urls( self ):
		return self.lista_urls

	def get_lista_ids( self ):
		return self.lista_ids

	def get_lista_lastmod( self ):
		return self.lista_lastmod

	def get_dict_id_elem( self ):
		return self.dict_id_elem

	def get_dict_lastmod_elem( self ):
		return self.dict_lastmod_elem

	def get_len_lista_ids( self ):
		return len(self.lista_ids)
	
	def get_len_lista_lastmod( self ):
		return len(self.lista_lastmod)
		
	def getStatusSitemapUpdate(self):
		
		result = {}
		result['initdate'] = self.get_lista_lastmod()[0]
		result['enddate'] = self.get_lista_lastmod()[-1]
		result['items'] = self.get_len_lista_lastmod()

		return result


	def getStatusSitemap(self):
		result = {}
		if self.get_len_lista_ids() > 0:
			result['initid'] = self.lista_ids[0]
			result['endid'] = self.lista_ids[-1]
			result['initdate'] = self.get_urls_values( self.dict_id_elem[ result['initid'] ])['lastmod']
			result['initdate'] = pyTools.ritornDateSitemapDecimal( result['initdate'] )
			result['enddate'] = self.get_urls_values( self.dict_id_elem[ result['endid'] ])['lastmod']
			result['enddate'] = pyTools.ritornDateSitemapDecimal( result['enddate'] )
			result['items'] = self.get_len_lista_ids()
		else:
			result['initid'] = -1
			result['endid'] = -1
			result['items'] = -1


		return result

	def remove_elem(self, id):

		logger.debug('---------------- INIT remove_elem --------------------')
		logger.debug('---------------- INIT remove_elem --------------------')
		if len(self.lista_urls) < 1:
			return None
		# togliere ultimo item da
		# xml
		result = id
		logger.debug('result = ' + str(result))
		self.root.remove( self.dict_id_elem[ id ] )
		# lista id
		lastItemId = id
		#logger.debug(lastItemId )
		self.lista_ids.remove(lastItemId) 
		#logger.debug(self.lista_ids)
		
		# dict id_elem
		del self.dict_id_elem[ lastItemId ]
		#logger.debug( self.dict_id_elem )
		logger.debug('---------------- END remove_elem --------------------')
		logger.debug('---------------- END remove_elem --------------------')

		return result


	def pop_last_elem(self):

		logger.debug('---------------- INIT pop_last_elem --------------------')
		logger.debug('---------------- INIT pop_last_elem --------------------')
		if len(self.lista_urls) < 1:
			return None
		# togliere ultimo item da
		# xml
		logger.debug('lista_ids : ' + str(self.lista_ids))
		result = self.lista_urls[-1]
		logger.debug('result = ' + str(result))
		self.root.remove( result )
		# lista id
		lastItemId = self.lista_ids[-1]
		#logger.debug(lastItemId )
		self.lista_ids.remove(lastItemId) 
		#logger.debug(self.lista_ids)
		
		# dict id_elem
		del self.dict_id_elem[ lastItemId ]
		#logger.debug( self.dict_id_elem )
		logger.debug('---------------- END pop_last_elem --------------------')
		logger.debug('---------------- END pop_last_elem --------------------')

		return result

	def dumpDoc(self):
		#tree = ET.ElementTree(self.root)
		#ET.dump(tree)
		logger.debug(ET.tostring(self.root, encoding='unicode'))
	
	def getDocXml(self):
		return ET.tostring(self.root, encoding='unicode')

	def writeToFile( self, filename):
		tree=ET.ElementTree(self.root) 
		tree.write(filename, xml_declaration=True, method='xml')

	def crea_lista_ids(self):
		_tmplist = []
		if self.lista_urls is None:
			self.lista_urls = self.root.findall( namespaces['xmlns'] + "url" )
		for lis in self.lista_urls:
			#for child in lis:
				#logger.debug(child.tag, child.attrib)
			#logger.debug(lis)
			loc = lis.find(namespaces['xmlns'] + "loc")
			#logger.debug(loc.text)
			#logger.debug(loc.text.split('--')[-1].replace('.html1','').replace('.html',''))
			_tmplist.append(int(loc.text.split('--')[-1].replace('.html1','').replace('.html','')))
		self.lista_ids = sorted(_tmplist)

	def crea_dict_all(self):
		if self.lista_urls is None:
			self.lista_urls = self.root.findall( namespaces['xmlns'] + "url" )
		for lis in self.lista_urls:
			#for child in lis:
				#logger.debug(child.tag, child.attrib)
			#logger.debug(lis)
			loc = lis.find(namespaces['xmlns'] + "loc")
			#logger.debug(loc.text)
			#logger.debug(loc.text.split('--')[-1].replace('.html1','').replace('.html',''))
			self.dict_id_elem[ int(loc.text.split('--')[-1].replace('.html1','').replace('.html',''))] = lis 

			lastmod = lis.find(namespaces['xmlns'] + "lastmod")
			lastmodint = pyTools.ritornDateSitemapDecimal( lastmod.text )
			self.dict_id_lastmod[ int(loc.text.split('--')[-1].replace('.html1','').replace('.html',''))] = lastmodint 

	def crea_lista_lastmod(self):
		_tmplist = []
		if self.lista_urls is None:
			self.lista_urls = self.root.findall( namespaces['xmlns'] + "url" )
		for lis in self.lista_urls:
			#for child in lis:
				#logger.debug(child.tag, child.attrib)
			#logger.debug(lis)
			_tmplist.append(lastmodint)
		self.lista_lastmod = _tmplist


	def crea_dict_lastmod_elem(self):
		if self.lista_urls is None:
			self.lista_urls = self.root.findall( namespaces['xmlns'] + "url" )
		for lis in self.lista_urls:
			#for child in lis:
				#logger.debug(child.tag, child.attrib)
			#logger.debug(lis)
			lastmod = lis.find(namespaces['xmlns'] + "lastmod")
			lastmodint = pyTools.ritornDateSitemapDecimal( lastmod.text )
			self.dict_lastmod_elem[lastmodint] = lis


	def remove_lista_urls(self):
		logger.debug('----------------- INIT remove_lista_urls')
		#self.dumpDoc()
		for lis in self.lista_urls:
			#logger.debug(lis.tag, lis.text)
			self.root.remove(lis)
		#self.dumpDoc()
		logger.debug('----------------- END remove_lista_urls')
			
			
	def get_urls_values( self, elem ):

		#logger.debug('---------------- INIT get_urls_values --------------------')
		#logger.debug('---------------- INIT get_urls_values --------------------')
		result = {}
		#logger.debug(ET.tostring(elem))

		# adesso devo prendere i valore dell id dalla loc
		loc = elem.find(namespaces['xmlns'] + "loc")
		result['loc'] = loc.text
		#logger.debug(loc.text)
		#logger.debug(loc.text.split('--')[-1].replace('.html1','').replace('.html',''))
		__elem_id = (int(loc.text.split('--')[-1].replace('.html1','').replace('.html','')))
		#logger.debug(__elem_id)
		result['id'] = __elem_id
		lastmod = elem.find(namespaces['xmlns'] + "lastmod")
		result['lastmod'] = lastmod.text
		#logger.debug(result)
		
		return result
		logger.debug('---------------- END get_urls_values --------------------')
		#logger.debug('---------------- END get_urls_values --------------------')

	def prendi_vecchi( self, lastdate, limit ):
		result = []
		logger.debug(pyTools.sistemaDateSitemap(lastdate))
		# mi interessa sapere quanto e' il limite in milliseconds
		delta_limit = 86400000 * limit
		for key, value in self.dict_id_lastmod.items():
			#logger.debug(str(key) + ' - ' + str(value))		
			#logger.debug(str(key) + ' - ' + pyTools.sistemaDateSitemap(value))		
			delta_value = 0
			delta = (lastdate - value ) - delta_limit
			#logger.debug( lastdate - value ) 
			#logger.debug( delta_limit )
			if  delta > 0:
				result.append( key )
		logger.debug(result)
		return result
	
	def prendi_vecchi_elem( self, lastdate, limit ):
		tmpresult = []
		result = []
		logger.debug(pyTools.sistemaDateSitemap(lastdate))
		# mi interessa sapere quanto e' il limite in milliseconds
		delta_limit = 86400000 * limit
		for key, value in self.dict_id_lastmod.items():
			#logger.debug(str(key) + ' - ' + str(value))		
			#logger.debug(str(key) + ' - ' + pyTools.sistemaDateSitemap(value))		
			delta_value = 0
			delta = (lastdate - value ) - delta_limit
			#logger.debug( lastdate - value ) 
			#logger.debug( delta_limit )
			if  delta > 0:
				tmpresult.append( key )

		logger.debug(tmpresult)
		dict_elem = self.get_dict_id_elem()
		for id in tmpresult:
			result.append( dict_elem[ id ] )
		return result
	



	def prendi_remove_vecchi_elem( self, lastdate, limit ):
		tmpresult = []
		result = []
		logger.debug(pyTools.sistemaDateSitemap(lastdate))
		# mi interessa sapere quanto e' il limite in milliseconds
		delta_limit = 86400000 * limit
		for key, value in self.dict_id_lastmod.items():
			#logger.debug(str(key) + ' - ' + str(value))		
			#logger.debug(str(key) + ' - ' + pyTools.sistemaDateSitemap(value))		
			delta_value = 0
			delta = (lastdate - value ) - delta_limit
			#logger.debug( lastdate - value ) 
			#logger.debug( delta_limit )
			if  delta > 0:
				tmpresult.append( key )

		logger.debug(tmpresult)
		dict_elem = self.get_dict_id_elem()
		for id in tmpresult:
			result.append( dict_elem[ id ] )
			self.remove_elem( id )
		return result
	

	def aggiungiElemDaXml( self, elem ):

		logger.debug('---------------- INIT aggiungiElemDaXml --------------------')
		#logger.debug('---------------- INIT aggiungiElemDaXml --------------------')
		logger.debug(ET.tostring(elem))

		# adesso devo prendere i valore dell id dalla loc
		loc = elem.find(namespaces['xmlns'] + "loc")
		#logger.debug(loc.text)
		#logger.debug(loc.text.split('--')[-1].replace('.html1','').replace('.html',''))
		__elem_id = (int(loc.text.split('--')[-1].replace('.html1','').replace('.html','')))
		#logger.debug(__elem_id)
		
		self.dict_id_elem[ __elem_id ] =  elem 
		# e lo metto anche nella lista degli id su cui lavorero
		self.lista_ids.append(__elem_id )
		#logger.debug( self.lista_ids )
		# adesso tolgo tutti quelli vecchi
		self.remove_lista_urls()
		# logger.debug(sorted(set(self.lista_ids)))
		# adesso devo solo ordinare la lista  degli id per avere la sequenza di elementi
		# uso sorted() + set() 
		# con set tolgo i duplicati qundi se eventualmente avevo ena entry duplicata 
		# vado poi a prendere quella nuova messa nel dict che avra' sovrascritto
		# quella precedente e cosi aggiorno il valore di lastmod
		self.lista_ids = sorted(set(self.lista_ids))
		for lis in self.lista_ids:
			# logger.debug( lis)
			# e creare un nuovo documento con gli elementi della lista ordinata
			self.root.append( self.dict_id_elem[ lis ] )

		self.lista_urls = self.root.findall( namespaces['xmlns'] + "url" )
		#logger.debug(self.lista_urls)
		logger.debug('---------------- END aggiungiElemDaXml --------------------')
		logger.debug('---------------- END aggiungiElemDaXml --------------------')

	def aggiungiCreaElem( self, value ):
		#logger.debug('---------------- INIT aggiungiCreaElem --------------------')
		#logger.debug('---------------- INIT aggiungiCreaElem --------------------')
		# devo verificare se esiste gia
		#if int(value['objectid']) in self.lista_ids:
			#logger.debug('gia presente il lista id : ' + value['objectid'])
			#logger.debug('gli cambio solo la lastmod ')
		# creo element da aggiungere
		__elem = ET.Element( namespaces['xmlns'] + "url" )
		__loc = ET.SubElement( __elem, namespaces['xmlns'] + "loc")
		__loc.text = value['loc']
		__lastmod = ET.SubElement( __elem, namespaces['xmlns'] + "lastmod")
		__lastmod.text = value['lastmod']
		#logger.debug(ET.tostring(__elem))
		self.dict_id_elem[ int(value['objectid']) ] =  __elem 
		# e lo metto anche nella lista degli id su cui lavorero
		#logger.debug( self.lista_ids )
		self.lista_ids.append(int(value['objectid']))
		#logger.debug( self.lista_ids )
		# adesso tolgo tutti quelli vecchi
		self.remove_lista_urls()
	
		# logger.debug(sorted(set(self.lista_ids)))
		# adesso devo solo ordinare la lista  degli id per avere la sequenza di elementi
		# uso sorted() + set() 
		# con set tolgo i duplicati qundi se eventualmente avevo ena entry duplicata 
		# vado poi a prendere quella nuova messa nel dict che avra' sovrascritto
		# quella precedente e cosi aggiorno il valore di lastmod
		self.lista_ids = sorted(set(self.lista_ids))
		for elem in self.lista_ids:
			#logger.debug( elem)
			# e creare un nuovo documento con gli elementi della lista ordinata
			self.root.append( self.dict_id_elem[ elem ] )

		
		self.lista_urls = self.root.findall( namespaces['xmlns'] + "url" )
		#self.dumpDoc()
		#logger.debug(self.lista_ids)
		#logger.debug('---------------- END aggiungiCreaElem --------------------')
		#logger.debug('---------------- END aggiungiCreaElem --------------------')


	def updateElemDaXml( self, elem ):

		logger.debug('---------------- INIT updateElemDaXml --------------------')
		#logger.debug('---------------- INIT updateElemDaXml --------------------')
		logger.debug(ET.tostring(elem))

		values = self.get_urls_values( elem ) 
		# adesso devo prendere i valore dell id dalla loc
		lastmod = pyTools.ritornDateSitemapDecimal( values['lastmod'] )
		#logger.debug(loc.text)
		self.dict_lastmod_elem[ lastmod ] =  elem 
		# e lo metto anche nella lista degli id su cui lavorero
		self.lista_lastmod.append(lastmod )
		#logger.debug( self.lista_ids )
		# adesso tolgo tutti quelli vecchi
		self.remove_lista_urls()
		# logger.debug(sorted(set(self.lista_ids)))
		# adesso devo solo ordinare la lista  degli id per avere la sequenza di elementi
		# uso sorted() + set() 
		# con set tolgo i duplicati qundi se eventualmente avevo ena entry duplicata 
		# vado poi a prendere quella nuova messa nel dict che avra' sovrascritto
		# quella precedente e cosi aggiorno il valore di lastmod
		self.lista_lastmod = sorted(set(self.lista_lastmod))
		for lis in self.lista_lastmod:
			# logger.debug( lis)
			# e creare un nuovo documento con gli elementi della lista ordinata
			self.root.append( self.dict_lastmod_elem[ lis ] )

		self.lista_urls = self.root.findall( namespaces['xmlns'] + "url" )
		#logger.debug(self.lista_urls)
		logger.debug('---------------- END updateElemDaXml --------------------')
		logger.debug('---------------- END updateElemDaXml --------------------')



	def updateCreaElem( self, value ):
		logger.debug('---------------- INIT updateCreaElem --------------------')
		logger.debug('---------------- INIT updateCreaElem --------------------')
		# devo verificare se esiste gia
		#if int(value['objectid']) in self.lista_ids:
			#logger.debug('gia presente il lista id : ' + value['objectid'])
			#logger.debug('gli cambio solo la lastmod ')
		# creo element da aggiungere
		__elem = ET.Element( namespaces['xmlns'] + "url" )
		__loc = ET.SubElement( __elem, namespaces['xmlns'] + "loc")
		__loc.text = value['loc']
		__lastmod = ET.SubElement( __elem, namespaces['xmlns'] + "lastmod")
		__lastmod.text = value['lastmod']
		#logger.debug(ET.tostring(__elem))
		self.dict_lastmod_elem[ int(value['lastModified']) ] =  __elem 
		# e lo metto anche nella lista degli id su cui lavorero
		#logger.debug( self.lista_ids )
		self.lista_lastmod.append(int(value['lastModified']))
		logger.debug(value)
		logger.debug(self.lista_lastmod)
		#logger.debug( self.lista_ids )
		# adesso tolgo tutti quelli vecchi
		self.remove_lista_urls()
	
		# logger.debug(sorted(set(self.lista_ids)))
		# adesso devo solo ordinare la lista  degli id per avere la sequenza di elementi
		# uso sorted() + set() 
		# con set tolgo i duplicati qundi se eventualmente avevo ena entry duplicata 
		# vado poi a prendere quella nuova messa nel dict che avra' sovrascritto
		# quella precedente e cosi aggiorno il valore di lastmod
		self.lista_lastmod = sorted(set(self.lista_lastmod))
		for elem in self.lista_lastmod:
			#logger.debug( elem)
			# e creare un nuovo documento con gli elementi della lista ordinata
			self.root.append( self.dict_lastmod_elem[ elem ] )

		
		self.lista_urls = self.root.findall( namespaces['xmlns'] + "url" )
		#self.dumpDoc()
		#logger.debug(self.lista_ids)
		logger.debug('---------------- END updateCreaElem --------------------')
		logger.debug('---------------- END updateCreaElem --------------------')

		


		




class xmlPiccoloParser(object):

	def __init__(self, contentXml):
		if isinstance( contentXml, (bytes) ):
			self.contentXml = contentXml.decode("utf-8") 
		else:
			self.contentXml = contentXml
		try:
			root = ET.fromstring(self.contentXml)
			self.root = root
			self.content =  self.root.findall(namespaces['atom'] + "content")[0]
			self.payload = self.content.findall(namespaces['vdf'] + "payload")[0]
			# for i in self.linkList:
			#     logger.debug(i.tag, "__", i.attrib)
		except Exception as e:
			logger.error( 'Error in __genRoot : ' + str(e) )
			return 

	def getRoot(self):
		return self.root

	def getXml(self):
		return self.contentXml

	def getPayload(self):
		return self.payload

	def getContent(self):
		return self.content

	def dumpDoc(self):
		#tree = ET.ElementTree(self.root)
		#ET.dump(tree)
		logger.debug(ET.tostring(self.root, encoding='unicode'))

	def writeToFile( self, filename):
		tree=ET.ElementTree(self.root) 
		tree.write(filename, xml_declaration=True, method='xml')

	def prendiField(self, rel):

		payload = self.content.findall(namespaces['vdf'] + "payload")[0]
		#logger.debug(payload.attrib)
		_fields = payload.findall( namespaces['vdf'] + "field")
		for idx , fiel in enumerate(_fields):
			#logger.debug(idx, fiel)
			#logger.debug(fiel.attrib['name'])
			if rel in fiel.attrib['name'] and len( rel) == len(fiel.attrib['name']):
				if fiel.find(namespaces['vdf'] + "value") is None:
					return None
				else:
					return fiel.find(namespaces['vdf'] + "value").text

		return None

	def cambiaField(self, entry , rel, value):

		self.content =  self.root.findall(namespaces['atom'] + "content")[0]
		payload = self.content.findall(namespaces['vdf'] + "payload")[0]
		#logger.debug(payload.attrib)
		_fields = payload.findall( namespaces['vdf'] + "field")
		for idx , fiel in enumerate(_fields):
			#logger.debug(idx, fiel)
			#logger.debug(fiel.attrib['name'])
			if rel in fiel.attrib['name'] and len( rel) == len(fiel.attrib['name']):
				if fiel.find(namespaces['vdf'] + "value") is None:
					fiel.append(ET.Element(namespaces['vdf'] + "value"))
				fiel.find(namespaces['vdf'] + "value").text = value
				return entry

		return entry

	def getState( self ):
		logger.debug(' - init  getState')
		lista = self.root.findall(namespaces['app'] + "control/" + namespaces['vaext'] + 'state')
		for idx, lis in enumerate(lista):
			if 'approved' in lis.attrib['name']:
				return 'draft'
			else:
				return lis.attrib['name']
		return None


	def getModel( self ):
		logger.debug(' - init  getModel')

		# estrazione del model
		model = self.payload.attrib["model"].split("/")[-1]

		#prendo l'id dell'elemento corrente se non e unresolved
		if 'unresolved' in model:
			logger.error('ERROR')
			return ''

		return model



	def cambiaSubtitleUrl( self ):
		# questa fa la replace seguenti
		# replace('https://coredelivery.rsi.ch/subtitles/','https://rsi-subtitles.s3.eu-central-1.amazonaws.com/')
		# replace('https://coredelivery.rsi.ch/subtitles//','https://rsi-subtitles.s3.eu-central-1.amazonaws.com/')
		# replace('https://cdn.rsi.ch/subtitles/','https://rsi-subtitles.s3.eu-central-1.amazonaws.com/')
		# replace('https://cdn.rsi.ch/subtitles//','https://rsi-subtitles.s3.eu-central-1.amazonaws.com/')
		val = self.prendiField( 'subtitleUrl' ) 

		if val is None:
			return None

		val = val.replace('https://coredelivery.rsi.ch/subtitles//','https://rsi-subtitles.s3.eu-central-1.amazonaws.com/')
		val = val.replace('https://coredelivery.rsi.ch/subtitles/','https://rsi-subtitles.s3.eu-central-1.amazonaws.com/')
		val = val.replace('https://cdn.rsi.ch/subtitles//','https://rsi-subtitles.s3.eu-central-1.amazonaws.com/')
		val = val.replace('https://cdn.rsi.ch/subtitles/','https://rsi-subtitles.s3.eu-central-1.amazonaws.com/')

		tree = self.cambiaField( self.root, 'subtitleUrl', val )
		tree = ET.ElementTree(tree)
		return tree 

	def prendiHomeSectionDaProgramme( self ):
		logger.debug ( '------------------------ INIT prendiHomeSectionDaProgramme -------------- ' )
		logger.debug( '------------------------ INIT prendiHomeSectionDaProgramme -------------- ' )
		result = -1
		try:
			link = self.prendiListaRelated( "home-section" )
			if not(link  is None):
				logger.debug ( link[0])
				logger.debug ( link[0].attrib['href'].split('section/')[-1])
				# da mettere un po di controllo errori ....
				result =  link[0].attrib['href'].split('section/')[-1]

		except Exception as e:
			logger.debug ( 'PROBLEMI in prendiHomeSectionDaProgramme : ' + str(e) )
			return result

		logger.debug ( '------------------------ END prendiHomeSectionDaProgramme -------------- ' )
		logger.debug( '------------------------ END prendiHomeSectionDaProgramme -------------- ' )
		return result


	def prendiSectionDaProgramme( self ):
		logger.debug( '------------------------ INIT prendiSectionDaProgramme -------------- ' )
		logger.debug( '------------------------ INIT prendiSectionDaProgramme -------------- ' )
		# nuova versione che prende i valori dal padre per ricalcolarsela
		# per sistemare robe tipo falo->falo estate ....
		jsonForSection = {}
		
		result = -1

		tmpVal = self.prendiField( 'channel')
			
		if tmpVal is None or len(tmpVal) < 1:
			logger.debug( "ritorno -1 perche tmpVal CHANNEL e nullo")
			logger.warning( "ritorno -1 perche tmpVal CHANNEL e nullo")
			jsonForSection['channel'] = ''
		else:
			jsonForSection['channel'] = tmpVal

		tmpVal = self.prendiField( 'parentSeries')
		if tmpVal is None or len(tmpVal) < 1:
			logger.debug( "ritorno a prendere il valore dal link della homesection perche tmpVal PARENTSERIES era nullo")
			logger.debug( "ritorno a prendere il valore dal link della homesection perche tmpVal PARENTSERIES era nullo")
			# non devo tornare bensi usare il metodo vecchio 
			# ed andare a prenderlo dal link con home-section
			return self.prendiHomeSectionDaProgramme( )
		else:
			jsonForSection['__DA_PASSARE_A_BRAND__'] = tmpVal

		tmpVal = self.prendiField( 'episode_producttypedesc')
		if not (tmpVal is None ) and len(tmpVal) > 1:
			# questo non e' indispensabile
			# quindi se non c'e' non importa
			jsonForSection['__PRODUCTTYPEDESC_MAMPROGRAMME__'] = tmpVal

		result = pyTools.prendiSectionId(jsonForSection)

		logger.debug( '------------------------ END prendiSectionDaProgramme -------------- ' )
		logger.debug( '------------------------ END prendiSectionDaProgramme -------------- ' )
		return result

	def prendiLeadId( self, rel):
		logger.debug( '------------------------ INIT prendiLeadId -------------- ' )
		logger.debug( '------------------------ INIT prendiLeadId -------------- ' )
		result = ''
		
		# al momento prende sempre e solo la prima
		# e assume che sia una immagine

		list =  self.root.findall(namespaces['atom'] + "link")

		#logger.debug(len(list))

		for idx , lis in enumerate(list):
			#logger.debug(idx, lis)
			#logger.debug(lis.attrib['rel'])
			if rel in lis.attrib['rel']:
				#for idx2, attr in enumerate(lis.attrib):
					#logger.debug(idx2, attr)
				#logger.debug(lis.attrib[namespaces['metadata'] + 'group'])
				group =  lis.attrib[namespaces['metadata'] + 'group']
				if 'lead' in group:
						#logger.debug(lis.attrib['href'])
						#logger.debug(lis.attrib[namespaces['dcterms'] + 'identifier'])
						return lis.attrib[namespaces['dcterms'] + 'identifier']

		return result

	def prendiDateUpdate( self ):

		result = ''
		list =  self.root.findall(namespaces['atom'] + "updated")
		for lis in list:
			return lis.text
		
		return result

	def prendiListaRelated(self, rel):

		result = []
		list =  self.root.findall(namespaces['atom'] + "link")
		for idx , lis in enumerate(list):
			#logger.debug(idx, lis)
			#logger.debug(lis.attrib['rel'])
			if rel in lis.attrib['rel']:
				result.append( lis )
		return result

	def verificaUpdateProgramme( self, leadId ):
		logger.debug( '------------------------ INIT verificaUpdateProgramme -------------- ' )
		logger.debug( '------------------------ INIT verificaUpdateProgramme -------------- ' )
		result = False
		idFromLead = -1
			
		# devo prendere l identifier della relazione in lead 
		idFromLead = self.prendiLeadId( 'related')


		# e quindi vedere se e diversa da leadId
		if leadId in idFromLead:
			logger.debug(' stesso id nel lead non faccio nulla' )
			logger.debug(' stesso id nel lead non faccio nulla' )
		else:
			logger.debug(' id diversi metto leadId = ' + leadId + ' in cima alle lead')
			logger.debug(' id diversi metto leadId = ' + leadId + ' in cima alle lead')
			return True

		logger.debug( '------------------------ END verificaUpdateProgramme -------------- ' )
		logger.debug( '------------------------ END verificaUpdateProgramme -------------- ' )
		return result

	def prendiInfoDaEce( self ):

		logger.debug(' ---------- INIT prendiInfoDaEce -------------- ')
		result = {}
		listaChannels = []

		try:
			listaEce = listaFields.listaLiveFields
			for lis in listaEce:
				result[ lis ] = self.prendiField( lis )

			# quindi devo prendere le info dei social
			for chan in listaFields.listaLiveChannel:
				result[ chan ] = prendiSocialInfo( entry, chan )
				logger.debug( result[ chan ]  )
				for key, value in result[chan].items():
					listaChannels.append( key )
			
			#logger.debug(result)
		except Exception as e:
			logger.debug(' EXCEPTIOOOONNNNNN - in prendiInfoDaEce !!!! ' + str(e))
			return [ {} , [] ]
		logger.debug(' ---------- FINE prendiInfoDaEce -------------- ')
		return [ result, listaChannels ]



	def prendiSocialInfo( self, entry, fieldName ):

		result = {}
		list =  entry.findall(namespaces['atom'] + "content")
		for lis in list:
			#logger.debug(lis)
			payload =  lis.findall(namespaces['vdf'] + "payload")
			for pay in payload:
				fields = pay.findall(namespaces['vdf'] + "field")
				#logger.debug(fields)

				for idx , fiel in enumerate(fields):
					#logger.debug(idx, fiel)
					#logger.debug(fiel.attrib['name'])
					if fieldName == fiel.attrib['name']:
						#logger.debug('passo di qui')
						# qui ho preso il field fb-livestreaming-account
						# e adesso devo prendere tutti gli account che ho messo
						_list = fiel.findall(namespaces['vdf'] + "list")
						if len(_list) > 0:
							_list = _list[0]
						else:
							return result

						stre_payloads =  _list.findall(namespaces['vdf'] + "payload")
						logger.debug('stre_payloads ')
						logger.debug(stre_payloads)
						for stre in stre_payloads:
							tmpResult = {}
							logger.debug('giro _payloads')
							# per ogni payload della lista dei social di quel canale
							# devo prima prendere il field capo che si chiama come fieldName
							stre_field = stre.find(namespaces['vdf'] + "field")
							logger.debug( stre_field )
							if fieldName in stre_field.attrib['name']:
								logger.debug( 'passo')
								listaEce = listaFields.listaLiveSocial
								for lis in listaEce:
									tmpResult[ lis ] = self.prendiFieldSoc( stre_field, lis )
								result[ tmpResult['livesocialid'] ] = tmpResult


		return result


	def prendiFieldSoc( self, entry, name ):
		
		fields = entry.findall(namespaces['vdf'] + "field")

		for idx , fiel in enumerate(fields):
			#logger.debug(idx, fiel)
			#logger.debug(fiel.attrib['name'])
			if name in fiel.attrib['name']:
				if not (fiel.find(namespaces['vdf'] + "value") is None) :
					return fiel.find(namespaces['vdf'] + "value").text
				else:
					return None

		return None

		


	def prendiKeyframesNames( self ):

		list =  self.root.findall(namespaces['atom'] + "link")

		#logger.debug(len(list))
		id_keyframe = []
		for idx , lis in enumerate(list):
			#logger.debug(idx, lis)
			#logger.debug(lis.attrib['rel'])
			if 'related' in lis.attrib['rel']:
				#for idx2, attr in enumerate(lis.attrib):
					#logger.debug(idx2, attr)
				#logger.debug(lis.attrib[namespaces['metadata'] + 'group'])
				group =  lis.attrib[namespaces['metadata'] + 'group']
	 
				if 'KEYFRAMES' in group:
					# ho trovato un keyframe
					_payload = lis.findall( namespaces['vdf'] + "payload")
					#logger.debug(_payload[0].attrib['model'])
					if 'EDITORIAL' in group:
					
						#  se editorial non lo tocco
						continue
					else:
						# se normale me lo ricordo 
						id_keyframe.append(lis.attrib['title'] )

		return id_keyframe


	def sistemaDurationMigrAudio( self, eceid ):

		
		valDur = 0
		valTM = self.prendiField( 'transcoderMetadata' )
		logger.debug(valTM)
		if valTM is None:
			logger.error('transcoderMetadata ERROR su : ' + str(eceid))
			exit(0)
		else:

			# altrimenti se esiste devosolo modificarlo e quindi cerco la duration nella source
			
			# altrimenti se esiste devo solo modificarlo e quindi cerco la duration nella source
			audioStr = self.prendiField('audio').replace("\n","")
			audioJson = json.loads( audioStr )
			if 'source' in audioJson and not ( audioJson['source'] is None ) and 'duration' in audioJson['source']:
				# se esiste il campo duration dalla source lo prendo da li
				valDur = audioJson['source']['duration']
			else:
				# alrimenti devo cmq chiamare il play per prenderlo da li
				# siamo gia passati dal PLAY e non ci serve piu il valore intero
				# quindi ritorno ok  -> da capire come fare
				valDur = self.prendiField('duration')
			valDur = self.myFloat(valDur)
			if valDur is None:
				valDur = self.prendiPlayAudioDuration(eceid)
				valDur = self.myFloat(valDur)
				if valDur is None:
					logger.error('ECE_PLAY ERROR su : ' + str(eceid))
					return None

			jsonTM = json.loads(valTM.replace('\'','\"'))
			logger.debug(jsonTM)
			_tmeta = []
			if 'transcodedAssets' in jsonTM:
				for _ta in jsonTM['transcodedAssets']:
					logger.debug(_ta['duration'])
					_ta['duration'] = valDur*1000.0
					_tmeta.append( _ta )
			logger.debug(_tmeta)
			valTM = { "transcodedAssets": _tmeta, "status": "COMPLETED" }
			valTM =  json.dumps(valTM)
		
		logger.debug(valTM)
		logger.debug(valDur)
	
		tree = self.cambiaField( self.root, 'transcoderMetadata', valTM )
		#tree = self.cambiaField( self.root, 'transcoderMamStatus', 'ready' )
		tree = self.cambiaField( self.root, 'duration', str(valDur ))
		tree = ET.ElementTree(tree)
		#nome_file = '/home/perucccl/test.xml'
		#logger.debug(nome_file)
		#tree.write(nome_file)
		#exit(0)
		return tree



	def myFloat( self, num ):

		if num is None:
			return None
		try:
			return float(num)
		
		except Exception as e:
			logger.error( 'ERROR -> Error in myFloat : ' + str(e) )
			return None 

	def prendiLocation( self ):
		location = ''
		#logger.debug( ' Init prendiLocation')
		self.content =  self.root.findall(namespaces['atom'] + "content")[0]
		payload = self.content.findall(namespaces['vdf'] + "payload")[0]
		#logger.debug(payload.attrib)
		if 'model' in payload.attrib:
			#logger.debug(payload.attrib)
			location = payload.attrib['model']
		return location

	def prendiSectionParameters( self ):
		sectionaParam = ''
		self.content =  self.root.findall(namespaces['atom'] + "content")[0]
		_pay = self.content.findall(namespaces['vdf'] + "payload")[0]
		_fields = _pay.findall( namespaces['vdf'] + "field")
		for idx , fiel in enumerate(_fields):
			if ( 'com.escenic.sectionParameters' in fiel.attrib['name']) and (len( 'com.escenic.sectionParameters') == len(fiel.attrib['name'])):
				val = fiel.find(namespaces['vdf'] + "value")
				if val  is None:
					return
				sectionParam = val.text
		return sectionParam

	def cambiaSectionParameters( self, value ):
		sectionaParam = ''
		self.content =  self.root.findall(namespaces['atom'] + "content")[0]
		_pay = self.content.findall(namespaces['vdf'] + "payload")[0]
		_fields = _pay.findall( namespaces['vdf'] + "field")
		for idx , fiel in enumerate(_fields):
			if ( 'com.escenic.sectionParameters' in fiel.attrib['name']) and (len( 'com.escenic.sectionParameters') == len(fiel.attrib['name'])):
				_val = fiel.find(namespaces['vdf'] + "value")
				if _val  is None:
					#devo aggiungere un value
					logger.debug('devo aggiungere' )
					fiel.append(ET.Element(namespaces['vdf'] + "value"))
				logger.debug('metto valore ' + value)
				fiel.find(namespaces['vdf'] + "value").text = value

		return [ True, ET.ElementTree(self.root) ]

	def prendiListaEntry( self ):
		listaEntry = []
		
		entry =  self.root.findall(namespaces['atom'] + "entry")
		logger.debug ( entry )
	

	def prendiListaSubsections( self ):
		listaSections = []
		
		entry =  self.root.findall(namespaces['atom'] + "entry")
		#logger.debug ( entry )
		#logger.debug ( len(entry))
		for ent in entry:
			__identry = ent.find(namespaces['atom'] + 'id')
			#logger.debug(__identry)
			#logger.debug(__identry.text)
			listaSections.append((__identry.text).split('/')[-1])
		return listaSections

	def prendiSectionPath( self ):
		logger.info(' - init  prendiSectionPath')
		_tmpres = None

		linkList =  self.root.findall(namespaces['atom'] + "link")
		for link in linkList:
			dictAttr = link.attrib
			if ('rel' in dictAttr ) and ('alternate' in dictAttr['rel']):
				if 'href' in dictAttr:
					#logger.debug( dictAttr['href'].split('/')[-1])
					#_tmpres =  dictAttr['href'].split('/')[-1]
					_tmpres =  dictAttr['href']
					if 'https' in _tmpres:
						_httpPerSplit = 'https://'
					else:
						_httpPerSplit = 'http://'
					_tmpres = _tmpres.split(_httpPerSplit)[-1]
					_httpDaTogliere = _tmpres.split('/')[0]
					_tmpres = _tmpres.replace(_httpDaTogliere, '' )
		return _tmpres


	def prendiSectionDaProgramme( self ):
		logger.debug( '------------------------ INIT prendiSectionDaProgramme -------------- ' )
		logger.debug( '------------------------ INIT prendiSectionDaProgramme -------------- ' )
		# nuova versione che prende i valori dal padre per ricalcolarsela
		# per sistemare robe tipo falo->falo estate ....
		jsonForSection = {}
		
		result = -1

		tmpVal = self.prendiField('channel')
			
		if tmpVal is None or len(tmpVal) < 1:
			logger.debug( "ritorno -1 perche tmpVal CHANNEL e nullo")
			logger.warning( "ritorno -1 perche tmpVal CHANNEL e nullo")
			jsonForSection['channel'] = ''
		else:
			jsonForSection['channel'] = tmpVal

		tmpVal = self.prendiField( 'parentSeries')
		if tmpVal is None or len(tmpVal) < 1:
			logger.debug( "ritorno a prendere il valore dal link della homesection perche tmpVal PARENTSERIES era nullo")
			logger.debug( "ritorno a prendere il valore dal link della homesection perche tmpVal PARENTSERIES era nullo")
			# non devo tornare bensi usare il metodo vecchio 
			# ed andare a prenderlo dal link con home-section
			return self.prendiHomeSectionDaProgramme( )
		else:
			jsonForSection['__DA_PASSARE_A_BRAND__'] = tmpVal

		tmpVal = self.prendiField( 'episode_producttypedesc')
		if not (tmpVal is None ) and len(tmpVal) > 1:
			# questo non e' indispensabile
			# quindi se non c'e' non importa
			jsonForSection['__PRODUCTTYPEDESC_MAMPROGRAMME__'] = tmpVal

		result = pyTools.prendiSectionId(jsonForSection)

		logger.debug( '------------------------ END prendiSectionDaProgramme -------------- ' )
		logger.debug( '------------------------ END prendiSectionDaProgramme -------------- ' )
		return result
			
	def rimuoviListaRelated( self , rel):
		logger.debug ( '------------------------ INIT rimuoviListaRelated -------------- ' )
		# questa rimuove dal xml la lista delle relazioni 

		list =  self.root.findall(namespaces['atom'] + "link")
		for idx,lis in enumerate(list):
			#logger.debug(idx, lis)
			#logger.debug(lis.attrib['rel'])
			if rel in lis.attrib['rel']:
				#logger.debug('rimuovo qualcosa')
				self.root.remove( lis )
		logger.debug ( '------------------------ END rimuoviListaRelated -------------- ' )
		return
		
	def aggiungiEditorialList( self,editorialLink,thumbnailLink, listaRel ):
		
		logger.debug ( '------------------------ INIT aggiungiEditorialList -------------- ' )
		# questa ritorna una stringa con la lista delle related ordinata
		# per il valore che trova in custom

		listaLink = []
		list =  self.root.findall(namespaces['atom'] + "link")
		for idx,lis in enumerate(list):
			#logger.debug(idx, lis)
			listaLink.append( lis )
			self.root.remove(lis)

		primoRel = True
		for llink in listaLink:
			if primoRel and 'related' in llink.attrib['rel'] and 'editorialkeyframes' in  llink.attrib['metadata:group']:
				
				# aggiungo quello nuovo prima degli altri eventuali editorial
				self.root.append(thumbnailLink )
				self.root.append(editorialLink )
				for rel in listaRel:
					self.root.append(rel)
				primoRel = False
			if primoRel and 'storyline' in llink.attrib['rel']:
				# aggiungo quello nuovo prima della story perche non ci sono altri editorial 
				self.root.append(thumbnailLink )
				self.root.append(editorialLink )
				for rel in listaRel:
					self.root.append(rel)
				primoRel = False
			self.root.append(llink)

		logger.debug ( '------------------------ END aggiungiEditorialList -------------- ' )
		return 

		
	def creaRelationThumbnail(self, keyframeEceId ):
		__link = ET.Element('atom:link')
		__link.set('href',os.environ['CUE_THUMB'] + keyframeEceId)
		__link.set('rel','thumbnail')
		__link.set('type','image/png')
		
		return __link

	def creaRelationKeyframe(self, keyframeEceId, editorial ):
		__link = ET.Element('atom:link')
		__link.set('href',os.environ['CUE_CONTENT'] + keyframeEceId)
		__link.set('xmlns:vaext','http://www.vizrt.com/atom-ext')
		__link.set('xmlns:vdf','http://www.vizrt.com/types')
		__link.set('rel','related')
		__link.set('title','') 
		__link.set('type','application/atom+xml; type=entry')
		__link.set('dcterms:identifier',keyframeEceId)	
		__link.set('metadata:group',"editorialkeyframes" if editorial else "keyframes")
		__link.set('metadata:synthetic-id','')
		__link.set('metadata:thumbnail',os.environ['CUE_THUMB'] + keyframeEceId)
		__link.set('vaext:state','published')
		__payload = ET.SubElement( __link, 'vdf:payload')
		__payload.set('model',os.environ['CUE_CONTENTSUMMARY'] + 'picture' )
		#__caption = ET.SubElement( __payload, 'vdf:field')
		#__caption.set('name','caption')
		#__credits = ET.SubElement( __payload, 'vdf:field')
		#__credits.set('name','credits')
		#__crop = ET.SubElement( __payload, 'vdf:field')
		#__crop.set('name','crop')
		#__value = ET.SubElement( __crop, 'vdf:value')
		#__value.text = 'r16x9'
		
		return __link
	def addRelEditorialKeyframe(self, keyframeId ):
		# prendo la lista dei related
		listaRelated = self.prendiListaRelated("related")
		self.rimuoviListaRelated("related")
		self.aggiungiEditorialList()

if __name__ == "__main__":


	# 'ECE_USER' : 'TSMM', 'ECE_PWD':'8AKjwWXiWAFTxb2UM3pZ'

	os.environ['ECE_USER'] = 'TSMM'
	os.environ['ECE_USER'] = 'TSMM'
	os.environ['ECE_PWD'] = '8AKjwWXiWAFTxb2UM3pZ'

	ecePub = 'http://internal.publishing.staging.rsi.ch'
	ecePub = 'http://internal.publishing3.production.rsi.ch'
	ecePre = 'http://presentation.staging.rsi.ch'
	ecePre = 'http://presentation5.rsi.ch'
	home = '/home/perucccl/STAGING/article-structure-mananager/'
	home = '/home/perucccl/PRODUCTION/article-structure-mananager/'

	os.environ['ECE_MODEL'] = ecePub + '/webservice/publication/rsi/escenic/model/'
	os.environ['IMG_CREATE_URL'] = ecePub + '/webservice/escenic/section/__CREATE_SECTION__/content-items'
	os.environ['ECE_SERVER'] = ecePub + '/webservice/escenic/content/'
	os.environ['ECE_SECTION'] = ecePub + '/webservice/escenic/section/'
	os.environ['ECE_BRAND'] = ecePub + '/webservice-extensions/srg/sectionIdForBrand/?publicationName=rsi&channel=__CHANNEL__&brand=__BRAND__'

	os.environ['CREATE_URL'] =  ecePub + "/webservice/escenic/section/__CREATE_SECTION__/content-items"
	os.environ['UPDATE_FILE'] =  "/home/perucccl/Webservices/STAGING/newMamServices/Resources/_cambiamento_"

	os.environ['ECE_ENTRIES'] = ecePre + '/live-center-presentation-webservice/event/__ECE_ID__/entries'
	os.environ['ECE_METADATA'] = ecePre + '/rsi-api/intlay/srgplay/migration/transcoder/metadata/'
	os.environ['ECE_PLAY'] = ecePre + '/rsi-api/intlay/srgplay/play/'
	os.environ['CUE_SECTION_FILES'] = home + '/LOGS/FILES/'
	os.environ['CUE_CREATE_FILES'] = home + '/LOGS/FILES/'
	os.environ['ECE_PACKAGING'] = 'http://packaging.rsi.ch/media-delivery/audio/ww/'
	os.environ['MEDIA_PATH'] = '/mnt/rsi_transcoded/vmeo/httpd/html/'


	#eceId = '13446031' #VME Vide
	#eceId = '20998' # migV
	eceId = '283092' # oldPV
	eceId = '4904' # oldPV

	#eceId = '1897266' # oldPV
	#eceId = '164759' # oldPV
	#eceId = '30481' # oldPV
	eceId = '291122' # oldPA
