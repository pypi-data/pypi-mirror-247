import logging
import xml.etree.ElementTree
import xml.etree.ElementTree as ET
import os
import json
import re

from datetime import datetime

import rsi_python_lib.pyCueServices as cueServices
import rsi_python_lib.xmlService as xmlService
import rsi_python_lib.pyTools as pyTools

from operator import itemgetter
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
		#'': '{http://www.w3.org/1999/xhtml}',
		'playout' : '{http://ns.vizrt.com/ardome/playout}' }




logger = logging.getLogger()


for entry in namespaces:
        #logger.debug(entry, namespaces[entry])
        ET._namespace_map[namespaces[entry].replace('{','').replace('}','')] = entry

class MasterType():
	def __init__(self):
		logger.debug("never called in this case")

	def __new__(self, cueId = None, cType = None, assetdata = None):
		logger.debug( 'MASTER' )
		__content = None
		__eTag = None

		if not (cueId is None):
			logger.debug('Passo da CueId')
			# devo andare a leggere xml di quel cueId 
			# vedere di che tipo e
			# e far partire la load del contenType opportuno
			[ successGetId, resultContent, __eTag  ] =  cueServices.getId( cueId )
			if not successGetId:
				return [False, {"error" : "Non trovato EceId di riferimento" }]
			# e adesso guardo di che tipo e'
			xmlParser = xmlService.xmlPiccoloParser( resultContent )
			__model = xmlParser.getModel()
			logger.debug(__model)



		if not (cType is None):
			logger.debug('Passo da cType')
			__model = cType
			# devo ritornare l'istanza di contenType opportuna
		if not (assetdata is None):
			if 'oldType' in assetdata:
				logger.debug( 'passo da assetdata: ' + assetdata['oldType'] )
				__model = assetdata['oldType'] 
			else:
				logger.debug('NON so CHI SONO !!! ' )
				return [False, {"error" : "Non ho capito chi sono" }]

		if 'keyframe' in __model or 'picture' in __model: 
			__content = Keyframe()
		elif 'programmeVideo'  in __model and len(__model) == len('programmevideo'): 
			__content = ProgrammeVideo()
		elif 'programmeAudio'  in __model and len(__model) == len('programmeaudio'): 
			__content = ProgrammeAudio()
		elif 'transcodableVideo'  in __model and len(__model) == len('transcodableVideo'): 
			__content = TranscodableVideo()
		elif 'video'  in __model and len(__model) == len('video'): 
			__content = Video()
		elif 'audioProgramme'  in __model and len(__model) == len('audioProgramme'): 
			__content = AudioProgramme()
		elif 'videoProgramme'  in __model and len(__model) == len('videoProgramme'): 
			__content = VideoProgramme()
		elif 'videosegment'  in __model and len(__model) == len('videosegment'): 
			__content = VideoSegment()
		elif 'audiosegment'  in __model and len(__model) == len('audiosegment'): 
			__content = AudioSegment()
		elif 'audio'  in __model and len(__model) == len('audio'): 
			__content = Audio()
		elif 'livestreaming' in __model : 
			__content = Livestreaming()
		elif 'series' in __model : 
			__content = Series()
		elif 'story' in __model : 
			__content = Story()
		elif 'gallery' in __model : 
			__content = Gallery()
		elif 'recipe' in __model : 
			__content = Recipe()

		if __content is None:
			logger.debug('nessuna inizializzazione')
			return [False, {"error" : "Nessuna inizializzazione del content" }]
		
		if not (cueId is None):
			# e istanzio il contentType opportuno
			logger.debug('setto il content da cueId')
			__content.setRoot(xmlParser.getRoot())
			__content.setXml(xmlParser.getXml())
			__content.setPayload(xmlParser.getPayload())
			__content.setContent(xmlParser.getContent())
			__content.setETag(__eTag )
			__content.setCueId(cueId )

		if not (assetdata is None):
			logger.debug('setto assetdata ')
			__content.setAssetdata(assetdata)

		return  [ True, __content ]


		

class ContentType():


	def __init__(self):
		self.contentXml = None
		self.root = None
		self.payload = None
		self.content = None
		self.assetdata = None
		self.eTag = None
		self.model = None
		self.cueId = None

		self.listaFields = {}
		self.listaFieldsUpdate = {}
		# if len assetdata < 1 ritorno ?
		# e adesso deve vedere se si tratta si una create o di una retrieve

	def getDoc(self):
		#tree = ET.ElementTree(self.root)
		#ET.dump(tree)
		return ET.tostring(self.root, encoding='unicode')

	def dumpDoc(self):
		#tree = ET.ElementTree(self.root)
		#ET.dump(tree)
		logger.warning(ET.tostring(self.root, encoding='unicode'))

	def writeToFile( self, filename):
		tree=ET.ElementTree(self.root) 
		tree.write(filename, xml_declaration=True, method='xml')

	def setETag(self, eTag):
		self.eTag = eTag

	def getETag(self):
		return self.eTag

	def setCueId(self, cueId):
		self.cueId = cueId

	def getCueId(self):
		return self.cueId

	def getModel(self):
		return self.model

	def setRoot(self, root):
		self.root = root

	def setPayload(self, contentPayload):
		self.payload = contentPayload


	def setContent(self, content):
		self.content = content


	def setXml(self, contentXml):
		self.contentXml = contentXml

	def setAssetdata(self, assetdata):
		logger.debug('setAssetdata')
		self.assetdata = assetdata

	def putToCue(self):
		nome_file = pyTools.creaNomeFile( self.model )
		logger.debug ( nome_file)
		self.writeToFile(nome_file)
		resultBool =  cueServices.putIdeTag( self.cueId, nome_file, self.getETag() )
		if not resultBool:
			logger.debug( " Errore in putId")
			return False
		else:
			logger.debug ( " updatato : " + self.cueId )
			return True

	def createNameSpaces(self):
		# crea le entry iniziali dei namespaces
		self.root = ET.Element("entry")
		self.root.set('xmlns','http://www.w3.org/2005/Atom')
		self.root.set('xmlns:app','http://www.w3.org/2007/app')
		#self.root.set('xmlns:vdf','http://www.vizrt.com/types')
		self.root.set('xmlns:metadata','http://xmlns.escenic.com/2010/atom-metadata')
		self.root.set('xmlns:dcterms','http://purl.org/dc/terms/')
		self.root.set('xmlns:age','http://purl.org/atompub/age/1.0')

	def createPayload(self):
		content=ET.SubElement(self.root, 'content')
		content.set('type','application/vnd.vizrt.payload+xml')
		self.payload=ET.SubElement(content, 'vdf:payload')
		self.payload.set('xmlns:vdf','http://www.vizrt.com/types' )

	def createState(self, state):
		# crea la entry per lo state

		__appControl = ET.SubElement(self.root, 'app:control');
		if 'draft' in state and len('draft') == len(state):
			__appDraft = ET.SubElement(__appControl, 'app:draft')
			__appDraft.text = "yes"
			# TODO DEBUG da capire cosa manca mettere  ....

		elif 'published' in state and len('published') == len(state):
			__vaextState =  ET.SubElement(__appControl, 'vaext:state')
			__vaextState.text = "published"
			__vaextState.set('xmlns:vaext','http://www.vizrt.com/atom-ext')

	def prendiStateActive( self ):
		logger.debug('-------- INIT prendi StateActive -----------')
		list =  self.root.findall(namespaces['app'] + "control/" + namespaces['vaext'] + 'state')
		active = True
		if len(list) > 1:
			logger.debug( list[0].attrib['name'] )
			if 'post-active' in list[1].attrib['name'] : 
				active = False 
			return [  list[0].attrib['name'], active ]
		else:
			return [ list[0].attrib['name'], active ]

	def prendi_lastmoddate( self ):
		logger.debug('-------- INIT prendi_lastmoddate -----------')
		list =  self.root.findall(namespaces['app'] + "edited")
		if len(list) > 0:
			return list[0].text
		else:
			return None

	def prendiState( self ):
		logger.debug('-------- INIT prendi State -----------')
		list =  self.root.findall(namespaces['app'] + "control/" + namespaces['vaext'] + 'state')
		for idx, lis in enumerate(list):
			return lis.attrib['name']


	def cambiaState( self, state ):
		logger.debug('-------- INIT cambia State -----------')
		list =  self.root.findall(namespaces['app'] + "control/" + namespaces['vaext'] + 'state')
		for idx, lis in enumerate(list):
			lis.text = state

	def createDateUpdated(self, date):
		__date = ET.SubElement(self.root, 'updated');
		__date.text = date

	def createDateAvailable(self, date):
		__date = ET.SubElement(self.root, 'dcterms:available');
		__date.text = date

	def createDateExpires(self, date):
		__date = ET.SubElement(self.root, 'age:expires');
		__date.text = date
				
	def sistemaRightsDates( self ):
		
		logger.debug ( '------------------------ INIT sistemaRightsDates del CONTENTTYPE -------------- ' )
		# e aggiungo tutta la trattazione dello starttime
		if 'rights_activationDate' in self.assetdata and not 'null' in self.assetdata['rights_activationDate'] and len(self.assetdata['rights_activationDate'] ) > 0:
			if 'Z' in self.assetdata['rights_activationDate']:
				logger.debug( 'arrivata rights_activationDate dal Programme' )
				# mi e' arrivata la data gia nel formato giusto
				data = self.assetdata['rights_activationDate']
				logger.debug( data )
				# se arriva da qui ha troppi zero primna della Z
			else :
				logger.debug( 'trovato rights_activationDate' )
				timestamp = int(self.assetdata['rights_activationDate'])/1000.0
				logger.debug( timestamp )
				value = datetime.utcfromtimestamp(timestamp)
				data = value.strftime("%Y-%m-%dT%H:%M:%SZ")
				logger.debug( data )

			logger.debug(len(data))

			# fix per formato data
			if len(data) == 24:
				# devo togliere i 3 valori prima della Z
				logger.debug(data[:-5]+ 'Z')
				data = data[:-5]+ 'Z'
				
			self.addUpdateVdfField( 'mediaactivedate', data )

		# e aggiungo tutta la trattazione del expire time
		if 'rights_expireDate' in self.assetdata and not 'null' in self.assetdata['rights_expireDate'] and len( self.assetdata['rights_expireDate']) > 0 :
			if 'Z' in self.assetdata['rights_expireDate']:
				logger.debug( 'arrivata rights_expireDate dal Programme' )
				# mi e' arrivata la data gia nel formato giusto
				data = self.assetdata['rights_expireDate'] 
				logger.debug( data )
			else:
				logger.debug( 'trovato rights_expireDate' )
				timestamp = int(self.assetdata['rights_expireDate'])/1000.0
				logger.debug( timestamp )
				value = datetime.utcfromtimestamp(timestamp)
				data = value.strftime("%Y-%m-%dT%H:%M:%SZ")
	
			# fix per formato data
			if len(data) == 24:
				# devo togliere i 3 valori prima della Z
				logger.debug(data[:-5]+ 'Z')
				data = data[:-5]+ 'Z'
				logger.debug( data )

			self.createDateExpires( data )
			self.addUpdateVdfField( 'mediaexpiredate', data )


	def getState( self ):
		logger.debug(' - init  getState')
		lista = self.root.findall(namespaces['app'] + "control/" + namespaces['vaext'] + 'state')
		for idx, lis in enumerate(lista):
			if 'approved' in lis.attrib['name']:
				return 'draft'
			else:
				return lis.attrib['name']
		return None


	def modifyState(self, state):

		list =  self.root.findall(namespaces['app'] + "control/" + namespaces['vaext'] + 'state')
		for idx , lis in enumerate(list):
			#logger.debug(idx, lis)
			lis.text = state
			return entry
		return None

	def createJsonSL( self, titolo , subhead, paragrafo, idSl):
		sLJson =   {"storyline" : { "model" : os.environ['CUE_STORYLINE'] + self.model,
		    "elements" : [ "/storyElements/1", 
				"/storyElements/2", 
				"/storyElements/3" ]
			  },
		  "storyElements" : {
		    "1" : {
		      "model" : os.environ['CUE_STORYELEMENTS'] + "toplabel",
		      "fields" : [ {
			"name" : "toplabel",
			"value" : "",
			"annotations" : [ ]
		      } ],
		    },
		    "2" : {
		      "model" : os.environ['CUE_STORYELEMENTS'] + "headline",

		      "fields" : [ {
			"name" : "headline",
			"value" : titolo,
			"annotations" : [ ]
		      } ]
		    }
		}
		}

		if subhead is None:
			sLJson['storyElements']['3'] = { "model" : os.environ['CUE_STORYELEMENTS'] + "subhead", "fields" : [ ] }
		else:
			sLJson['storyElements']['3'] = { "model" : os.environ['CUE_STORYELEMENTS'] + "subhead",
						      "fields" : [ {
							"name" : "subhead",
							"value" : subhead.replace("\r","\n"), # per evitare casini con \r !
							"annotations" : [ ]
						      } ]
						    }

		if not paragrafo is None:
			sLJson['storyline']['elements'].append("/storyElements/4")
			sLJson['storyElements']['4'] = {"model" : os.environ['CUE_STORYELEMENTS'] + "paragraph",
							"fields" : [ {
							"name" : "paragraph",
							"value" : paragrafo,
							"annotations" : [ ]
							} ]
							}
			
		if not idSl is None :
			sLJson['storyline']['id'] = idSl
			for _stKey, _stVal in sLJson['storyElements'].items():
				_stVal['id'] = idSl
				

		return json.dumps(sLJson)

	def getStoryLine(self):
		__listaLink =  self.root.findall(namespaces['atom'] + "link")
		for llink in __listaLink:
			if 'storyline' in llink.attrib['rel']:
				logger.debug('ritorno Storyline')
				return llink

		return None

	def removeStoryLine(self):
		__listaLink =  self.root.findall(namespaces['atom'] + "link")
		for llink in __listaLink:
			if 'storyline' in llink.attrib['rel']:
				logger.debug('rimuovo Storyline')
				__href =  llink.attrib['href']
				self.root.remove( llink )
				return __href.split('/')[-1]

		return None


	def createStoryLine(self, titolo, subhead, paragrafo, idSl ):
		__link = ET.SubElement(self.root,namespaces['atom']  + 'link')
		if not idSl is None:
			__link.set('href','https://cue.cue-test.rsi.ch/webservice/escenic/storyline/' + idSl)
		__link.set('rel','http://www.escenic.com/types/relation/storyline')
		__link.set('title',titolo) 
		__link.set('type','application/vnd.escenic.storyline+json')
	
		__link.text = self.createJsonSL(titolo, subhead, paragrafo, idSl)
		
		return __link

	def getFieldValue(self, fieldName ):
		return self.prendiFieldValue( fieldName )

	def prendiFieldValue( self, fieldName ):
		#self.dumpDoc()
		# restituisce il nodo di tipo field con quel nome
		# logger.debug ( '------------------------ inizia prendiFieldValue -------------- ' )	
		__fields = self.payload.findall("vdf:field")
		if len(__fields) == 0:
			__fields = self.payload.findall(namespaces['vdf'] + "field")
		#ET.dump(self.payload)
		for idx , fiel in enumerate(__fields):
			#logger.debug(idx, fiel)
			#logger.debug(fiel.attrib['name'])
			if fieldName in fiel.attrib['name'] and len(fieldName) == len( fiel.attrib['name'].strip()) :
				logger.debug('TROVATO')

				__fieldValue = fiel.find( namespaces['vdf'] +'value' )
				if not __fieldValue is None:
					return __fieldValue.text
				else:
					__fieldValue = fiel.find( 'vdf:value' )
					if not __fieldValue is None:
						return __fieldValue.text
					else:
						return None

		#logger.debug('NON TROVATO')
		return None

	def creaListaFields( self ):
		#self.dumpDoc()
		# creala lista di tutti i fields presenti nel self asset
		logger.debug ( '------------------------ inizia creaListaFields -------------- ' )	
		result = []
		__fields = self.payload.findall("vdf:field")
		if len(__fields) == 0:
			__fields = self.payload.findall(namespaces['vdf'] + "field")
		#ET.dump(self.payload)
		for idx , fiel in enumerate(__fields):
			#logger.debug(idx, fiel)
			#logger.debug(fiel.attrib['name'])
			result.append(fiel.attrib['name'])

		return result


	def prendiField( self, fieldName ):
		#self.dumpDoc()
		# restituisce il nodo di tipo field con quel nome
		logger.debug ( '------------------------ inizia prendiField -------------- ' )	
		__fields = self.payload.findall("vdf:field")
		if len(__fields) == 0:
			__fields = self.payload.findall(namespaces['vdf'] + "field")
		#ET.dump(self.payload)

		for idx , fiel in enumerate(__fields):
			#logger.debug(idx, fiel)
			#logger.debug(fiel.attrib['name'])
			if fieldName in fiel.attrib['name'] and len(fieldName) == len( fiel.attrib['name'].strip()) :
				logger.debug('Trovato: ' + fiel.attrib['name'] )
				#logger.debug( fiel  )
				return fiel

		logger.debug('NON Trovato')
		return None

	def prendiFieldOrder( self, entry ):

		#logger.debug (lis)
		
		logger.debug ( '------------------------ INIT prendiFieldOrder -------------- ' )
		payload =  entry.findall("vdf:payload")
		if len(payload) == 0:
			payload = entry.findall(namespaces['vdf'] + "payload")
		#logger.debug(len(payload))
		for pay in payload:
			fields = pay.findall("vdf:field")
			if len(fields) == 0:
				fields = pay.findall(namespaces['vdf'] + "field")
			#logger.debug(str(len(fields)))

			for idx , fiel in enumerate(fields):
				#logger.debug(idx, fiel)
				#logger.debug(fiel.attrib['name'])
				if 'order' in fiel.attrib['name']:
					#logger.debug('CLAD')
					if not (fiel.find(namespaces['vdf'] + "value") is None) :
						#logger.debug('CLAD value =' + fiel.find(namespaces['vdf'] + "value").text)
						return fiel.find(namespaces['vdf'] + "value").text
					else:
						#logger.debug('CLAD value = None')
						return -1

		return -1


	def addUpdateEntryField( self,  fieldName, fieldValue, fieldType):
		# aggiunge o eventualmente modifica il field entry

		# quindi cerca se sotto la entry ( cioe' la root ) 
		# esiste quel fieldName
		__entry =  self.root.find(fieldName)
		# se non trovo il nodo
		if __entry is None:
			if  len(fieldValue) < 1:
				return
			# allora lo creo e gli setto il valore
			__entry=ET.SubElement(self.root, fieldName)

		if not fieldType is None and len(fieldType) > 0:
			__entry.attrib['type'] = fieldType

		logger.debug( 'setto : ' + fieldValue)
		__entry.text = fieldValue 
		# altrimenti gli setto solo il valore

	def addUpdateVdfField( self, fieldName, fieldValue):
		# aggiunge o eventualmente modifica il field vdf
		# quindi cerca se sotto il payload ( cioe' la root ) 
		# esiste quel fieldName
		if len(fieldValue) > 0:
			logger.debug ( '------------------------ inizia addUpdateVdfField -------------- ' )	
			logger.debug ( fieldName + ' -> ' +  fieldValue )
			__field = self.prendiField( fieldName )
			# se non trovo il nodo
			logger.debug('__field : ' + str(__field ))
			if __field is None:
				# allora lo creo e poi gli setto il valore
				logger.debug('passo da None' )
				__field = ET.SubElement(self.payload, namespaces['vdf'] + 'field')
				__field.set('name', fieldName )
				__fieldValue = ET.SubElement( __field, namespaces['vdf'] + 'value' )
			else:
				logger.debug('passo da else' )
				__fieldValue = __field.find( 'vdf:value' )
				logger.debug('__fieldValue : ' + str(__fieldValue ))
				if  len(fieldValue) < 1:
					return
				logger.debug('__fieldValue in else : ' + str(__fieldValue ))
				if __fieldValue is None:
					__fieldValue = __field.find( namespaces['vdf'] + 'value' )
				if __fieldValue is None:
					__fieldValue = ET.SubElement( __field, 'vdf:value' )
			

			logger.debug( 'setto : ' + fieldValue)
			if  not ( fieldValue is None ) and len(fieldValue) > 0:
				__fieldValue.text = fieldValue 
				# altrimenti gli setto solo il valore




	def copyRelations(self):
		# sistema le reazioni lead e related
		logger.debug('copyRelations di contentType')
		return

	def createSections(self):
		# questo mette la homesection nel xml
		return

	def createDocument(self ):
		# crea il documento partendo da assetdata
		logger.debug(' super createDocument')
		self.createNameSpaces()
		self.createPayload()
		self.createSections()
		if 'title' in self.assetdata:
			self.addUpdateEntryField("title", self.assetdata['title'], "text")
		if 'summary' in self.assetdata:
			self.addUpdateEntryField("summary", self.assetdata['summary'], "text")
		if 'updated' in self.assetdata:
			self.addUpdateEntryField("updated", self.assetdata['updated'], None)

		if 'dcterms:available' in self.assetdata:
			self.addUpdateEntryField("dcterms:available", self.assetdata['dcterms:available'], None);
		if 'age:expires' in self.assetdata:
			self.addUpdateEntryField("age:expires", self.assetdata['age:expires'], None);
		# addUpdateEntryField("dcterms:available", activationDate, null);
		# addUpdateEntryField("age:expires", expirationDate, null);
		now = datetime.utcnow()
		#logger.debug(now.strftime("%Y-%m-%dT%H:%M:%SZ"))
		#self.addUpdateEntryField("pubdate", now.strftime("%Y-%m-%dT%H:%M:%SZ"), "text")
		self.addUpdateVdfField("pubdate", now.strftime("%Y-%m-%dT%H:%M:%SZ"))

		self.copyRelations();
	
				
	def updateListaFields( self, dictTochange ):
		# questa e' la mia updateListaFields

		logger.debug ( '------------------------ INIT updateListaFields -------------- ' )
		logger.debug ( '------------------------ INIT updateListaFields -------------- ' )
		count = 1

		for key,value in dictTochange.items():

			logger.debug ( key , type( value ) )
			if value is None or ( isinstance( value, str )  and len(value) < 1 ): 
					self.addUpdateVdfField( key, "")
			else:
				# il casino sui tipi qui sotto perche ECE accetta solo stringhe
				if isinstance( value , str):
					# aggiunto controllo per evitare passaggi di string = null
					if 'null' in value and len(value )<5:
						self.addUpdateVdfField( key, "" )
					else:
						self.addUpdateVdfField( key, value )
				else:
					if isinstance( value , bool):
						if value :
							#logger.debug ( 'bool' )
							self.addUpdateVdfField(key, 'true' )
						else:
							self.addUpdateVdfField(key, 'false' )
					else:
						if isinstance( value  ,int) or isinstance( value  ,float):
							#logger.debug ( 'int' )
							self.addUpdateVdfField(key,  str( value))
						else:
							if isinstance( value  ,dict):
								#logger.debug ( 'dic --------------------t' )
								# tmpval = str( value										
								tmpval = json.dumps( value )										
								tmpval =  tmpval.replace('True','true').replace('False','false') 
								self.addUpdateVdfField( key, tmpval )
		
		self.content =  self.root.findall(namespaces['atom'] + "content")[0]
		self.payload = self.content.findall(namespaces['vdf'] + "payload")[0]


		logger.debug ( '------------------------ END updateListaFields -------------- ' )
		logger.debug ( '------------------------ END updateListaFields -------------- ' )
	
		return

				
	def updateFields( self, jsonFlatRundown, fieldsMamProgramme ):
		# questa e' la mia updatefields

		logger.debug ( '------------------------ INIT updateFields -------------- ' )
		logger.debug ( '------------------------ INIT updateFields -------------- ' )
		count = 1

		logger.debug ( fieldsMamProgramme )
		logger.debug (jsonFlatRundown)
		for lis,value in fieldsMamProgramme.items():

			# questa qui sotto trova OGNI occorrenza della sottostringa lis nelle chiavi
			# del json mpJsonFlatRundown - anche forse troppo per quello che ci serve
			# res = dict(filter(lambda item: lis in item[0], mpJsonFlatRundown.items())) 
			# logger.debug (ing result   )
			# logger.debug (("Key-Value pair for substring keys : " + str(res))  )

			# come workaround facciamo che aggiungere schedule_broadcast_ a tutte le chiavi
			# per vedere se ci sono nell'altro

			if lis in jsonFlatRundown:
				#logger.debug ( jsonFlatRundown[ lis ], type( jsonFlatRundown[lis]) )
				if jsonFlatRundown[ lis ] is None or ( isinstance( jsonFlatRundown[lis], str )  and len(jsonFlatRundown[ lis ] ) < 1 ): 
					self.addUpdateVdfField( value, "")
				else:
					# il casino sui tipi qui sotto perche ECE accetta solo stringhe
					if isinstance( jsonFlatRundown[ lis ] , str):
						# aggiunto controllo per evitare passaggi di string = null
						if 'null' in jsonFlatRundown[ lis ] and len(jsonFlatRundown[ lis ] )<5:
							self.addUpdateVdfField( value, "" )
						else:
							self.addUpdateVdfField( value, jsonFlatRundown[ lis ] )
					else:
						if isinstance( jsonFlatRundown[ lis ] , bool):
							if jsonFlatRundown[ lis ] :
								#logger.debug ( 'bool' )
								self.addUpdateVdfField(value, 'true' )
							else:
								self.addUpdateVdfField(value, 'false' )
						else:
							if isinstance( jsonFlatRundown[ lis ]  ,int) or isinstance( jsonFlatRundown[ lis ]  ,float):
								#logger.debug ( 'int' )
								self.addUpdateVdfField(value,  str( jsonFlatRundown[lis ]))
							else:
								if isinstance( jsonFlatRundown[ lis ]  ,dict):
									#logger.debug ( 'dic --------------------t' )
									# tmpval = str( jsonFlatRundown[lis ])										
									tmpval = json.dumps( jsonFlatRundown[lis ])										
									tmpval =  tmpval.replace('True','true').replace('False','false') 
									self.addUpdateVdfField( value, tmpval )
			else:
				# per evitare che passino i valori di default
				# brutto fix per evitare che il dict sia inizializzato a '' anziche {}
				if '__TRANSCODERMETA' in value:
					self.addUpdateVdfField(value, '{}')
				else:
					self.addUpdateVdfField(value, '' )

		logger.debug ( '------------------------ END updateFields -------------- ' )
		logger.debug ( '------------------------ END updateFields -------------- ' )
	
	def prendiDateUpdate( self ):

		result = ''
		list =  self.root.findall(namespaces['atom'] + "updated")
		for lis in list:
			return lis.text
		
		return result

	def prendiListaSegmentsId(self):

		result = []
		list =  self.root.findall(namespaces['atom'] + "link")
		for idx , lis in enumerate(list):
			#logger.debug(idx, lis)
			#logger.debug(lis.attrib)
			if namespaces['metadata']+ 'group' in lis.attrib:
				if "segments" in lis.attrib[namespaces['metadata'] + 'group']:
					#logger.debug('segments')
					payload = lis.findall("vdf:payload")
					if len(payload)==0:
						payload = lis.findall(namespaces['vdf'] + 'payload')
					for pay in payload:
						if 'videosegment' in pay.attrib['model']:
							result.append(lis.attrib[namespaces['dcterms'] + 'identifier'])


		return result

	def prendiListaSegments(self):

		result = []
		list =  self.root.findall(namespaces['atom'] + "link")
		for idx , lis in enumerate(list):
			#logger.debug(idx, lis)
			#logger.debug(lis.attrib)
			if namespaces['metadata']+ 'group' in lis.attrib:
				if "segments" in lis.attrib[namespaces['metadata'] + 'group']:
					result.append(lis)


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

	def prendiPVideoIdDaRel(self, listaRel ):

		for entry in listaRel:
			payload =  entry.findall( "vdf:payload")
			for pay in payload:
				if 'mamProgrammeVideo' in pay.attrib['model']:
					#logger.debug('CLAD2')
					fields = pay.findall("vdf:field")
					if len(fields) == 0:
						fields = self.payload.findall(namespaces['vdf'] + "field")
					#logger.debug (entry.attrib[namespaces['dcterms'] + 'identifier'])
					#logger.debug (entry.attrib['href'])
					return entry.attrib[namespaces['dcterms'] + 'identifier']

		return None



	def rimuoviListaSegments( self):
		logger.debug ( '------------------------ INIT rimuoviListaSegments -------------- ' )
		# questa rimuove dal xml la lista delle relazioni 

		list =  self.root.findall(namespaces['atom'] + "link")
		for idx,lis in enumerate(list):
			#logger.debug(idx, lis)
			#logger.debug(lis.attrib['rel'])
			if namespaces['metadata'] + 'group' in lis.attrib:
				if "segments" in lis.attrib[namespaces['metadata'] + 'group']:
					logger.debug('rimuovo il segmento')
					self.root.remove( lis )
		logger.debug ( '------------------------ END rimuoviListaSegments -------------- ' )
		return
	


	def rimuoviListaRelated( self , rel):
		logger.debug ( '------------------------ INIT rimuoviListaRelated -------------- ' )
		# questa rimuove dal xml la lista delle relazioni 

		list =  self.root.findall(namespaces['atom'] + "link")
		for idx,lis in enumerate(list):
			logger.debug(idx, lis)
			#logger.debug(lis.attrib['rel'])
			if rel in lis.attrib['rel']:
				logger.debug('rimuovo qualcosa')
				self.root.remove( lis )
		logger.debug ( '------------------------ END rimuoviListaRelated -------------- ' )
		return
		
	def aggiungiEditorialList( self,editorialLink, listaRel ):
		
		logger.debug ( '------------------------ INIT aggiungiEditorialList -------------- ' )

		listaLink = []
		list =  self.root.findall(namespaces['atom'] + "link")
		for idx,lis in enumerate(list):
			#logger.debug(idx, lis)
			listaLink.append( lis )
			self.root.remove(lis)

		primoRel = True
		for llink in listaLink:
			logger.debug(llink.attrib['rel'])
			if primoRel and 'related' in llink.attrib['rel'] and 'editorialkeyframes' in  llink.attrib['metadata:group']:
				
				# aggiungo quello nuovo prima degli altri eventuali editorial
				self.root.append(editorialLink )
				for rel in listaRel:
					self.root.append(rel)
				primoRel = False
			if primoRel and 'storyline' in llink.attrib['rel']:
				logger.debug('passo da storyline')
				# aggiungo quello nuovo prima della story perche non ci sono altri editorial 
				self.root.append(editorialLink )
				for rel in listaRel:
					self.root.append(rel)
				primoRel = False
			self.root.append(llink)

		if primoRel:
			self.root.append(editorialLink )

		logger.debug ( '------------------------ END aggiungiEditorialList -------------- ' )
		return 
	

	def aggiungiSegmentiOrdinati( self, listaSegments ):
		
		logger.debug ( '------------------------ INIT aggiungiSegmentiOrdinati -------------- ' )
		order = {}
		result = ''
		#logger.debug(len(listaSegments))
		#logger.debug(listaSegments)
		for _segm in listaSegments:
			# in res ho la relazione 
			#logger.debug('_segm : ' + str( _segm ))
			#logger.debug('_segm to string : ' + str(ET.tostring(_segm )))
			#logger.debug ( self.prendiFieldOrder( _segm ) )
			order[ float(self.prendiFieldOrder( _segm )) ] = _segm

		#logger.debug( order )
		listaLink = []
		list =  self.root.findall(namespaces['atom'] +"link")
		for idx,lis in enumerate(list):
			#logger.debug(idx, lis)
			listaLink.append( lis )
			self.root.remove(lis)

		primoRel = True
		for llink in listaLink:
			if primoRel and 'storyline' in llink.attrib['rel']:
				#logger.debug('passo da storyline')
				# aggiungo quello nuovo prima della story perche non ci sono altri editorial 

				for i in sorted (order.keys()) :  
					#logger.debug(' giro su sorted order.keys -> ' + str(i))
					#logger.debug(' con valore : ' + ET.tostring(order[ i ] ))
					#exit(0)
					self.root.append( order[ i ] )

				primoRel = False
			self.root.append(llink)

		if primoRel:
	
			for i in sorted (order.keys()) :  
				#logger.debug(i)
				#logger.debug  (ET.tostring(order[ i ] ))
				#exit(0)
				self.root.append( order[ i ] )


		logger.debug ( '------------------------ END aggiungiSegmentiOrdinati -------------- ' )
		
	def creaRelationThumbnail(self, keyframeEceId ):
		__link = ET.Element(namespaces['atom'] + 'link')
		__link.set('href',os.environ['CUE_THUMB'] + keyframeEceId)
		__link.set('rel','thumbnail')
		__link.set('type','image/png')
		
		return __link

	def creaRelationKeyframe(self, keyframeEceId, group ):
		__link = ET.Element(namespaces['atom'] + 'link')
		__link.set('href',os.environ['CUE_CONTENT'] + keyframeEceId)
		__link.set('xmlns:vaext','http://www.vizrt.com/atom-ext')
		__link.set('xmlns:vdf','http://www.vizrt.com/types')
		__link.set('rel','related')
		__link.set('title','') 
		__link.set('type','application/atom+xml; type=entry')
		__link.set('dcterms:identifier',keyframeEceId)	
		__link.set('metadata:group', group )
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

	def creaRelationSegment(self, segmentId, order ):
		__link = ET.Element(namespaces['atom'] + 'link')
		__link.set('xmlns:vaext','http://www.vizrt.com/atom-ext')
		__link.set('xmlns:vdf','http://www.vizrt.com/types')
		__link.set('xmlns:atom','http://www.w3.org/2005/Atom')
		__link.set('xmlns:dcterms','http://purl.org/dc/terms/')
		__link.set('xmlns:metadata','http://xmlns.escenic.com/2010/atom-metadata')
		__link.set('href',os.environ['CUE_CONTENT'] + segmentId)
		__link.set('dcterms:identifier',segmentId)	
		__link.set('title','') 
		__link.set('rel','related')
		__link.set('type','application/atom+xml; type=entry')
		__link.set('metadata:group',"segments")
		__link.set('metadata:synthetic-id','')
		__link.set('vaext:state','published')
		__payload = ET.SubElement( __link, namespaces['vdf'] + 'payload')
		__payload.set('model',os.environ['CUE_CONTENTSUMMARY'] + 'videosegment' )
		__title = ET.SubElement( __payload, namespaces['vdf'] + 'field')
		__title.set('name','title')
		__subtitle = ET.SubElement( __payload, namespaces['vdf'] + 'field')
		__subtitle.set('name','subtitle')
		__crop = ET.SubElement( __payload, namespaces['vdf'] + 'field')
		__crop.set('name','crop')
		__value = ET.SubElement( __crop, namespaces['vdf'] + 'value')
		__value.text = 'r16x9'
		__order = ET.SubElement( __payload, namespaces['vdf'] + 'field')
		__order.set('name','order')
		__value = ET.SubElement( __order, namespaces['vdf'] + 'value')
		__value.text = str(float(order))
		return __link

	def getTags( self ):
		# questo sara un dict con
		# topic come chiave e la lista di tags per value
		result = {}
		__fieldTag = self.prendiField('com.escenic.tags')
		#logger.debug(__fieldTag)
		if __fieldTag is None:
			return result
		else:
			__tmplist = __fieldTag.findall(namespaces['vdf'] + "list")
			__list = __tmplist[0]
			#logger.debug(__list)
			__payloads = __list.findall(namespaces['vdf'] + "payload")
			for __pay in __payloads:
				#logger.debug(__pay)
				__fiel = __pay.findall(namespaces['vdf'] + "field")
				for idx , fiel in enumerate(__fiel):
					#logger.debug(idx, fiel)
					#logger.debug(fiel.attrib['name'])
					if 'tag' in fiel.attrib['name']:
						__origin = fiel.findall(namespaces['vdf'] + "origin")
						if len(__origin) > 0:
							# trovato una url la metto nella lista di quelle
							# da non duplicare
							for __ori in __origin:
								#logger.debug(__ori.attrib['href'].split('/')[-1])
								__href = __ori.attrib['href'].split('/')[-1]
								__topic = __href.split(',')[0]
								#logger.debug(__topic)
								__tag = __href.split(',')[-1]
								#logger.debug(__tag)
								if __topic in result:
									result[__topic].append( __tag )
								else:
									result[__topic] = [ __tag ]
						#logger.debug( fiel  )
			return result
	

	def updateTags(self):
		logger.debug(' INIT updateTags')
		# da verificare se lasciare solo __TAGS__ ... CLAD DEBUG
		if '__TAGS_MAMPROGRAMMEVIDEO__' in self.assetdata and len(self.assetdata['__TAGS_MAMPROGRAMMEVIDEO__']) >0:
			# devo aggiornare i tags cioe' aggiungere quelli che arrivano da kafka e non 
			# togliere quelli che sono stati messi in CUE
			# quindi verfico se ne esistono gia'

			old_tags = {}
			__fieldTag = self.prendiField('com.escenic.tags')
			#logger.debug(__fieldTag)
			if __fieldTag is None:
				__fieldTag = ET.SubElement( self.payload, 'vdf:field')
				__fieldTag.set('name','com.escenic.tags')
				__list = ET.SubElement( __fieldTag, 'vdf:list')
			else:
				__tmplist = __fieldTag.findall(namespaces['vdf'] + "list")
				__list = __tmplist[0]
				#logger.debug(__list)
				old_tags = self.getTags()
				# nel qual caso ne prendo la lista per evitare 
				# duplicati
				
			dict_from_file = {}	
			for __tag in self.assetdata['__TAGS_MAMPROGRAMMEVIDEO__']:
				# qui creo la lista dei tag che arrivano dal messaggio
				# sempre nella forma topic:[lista tags]
				for __topic in ['tag:srg.topic.rsi.ch','tag:hbbtv.topic.rsi.ch']:
					if __topic in dict_from_file:
						dict_from_file[__topic].append( __tag )
					else:
						dict_from_file[__topic] = [ __tag ]
			# adesso tolgo da quelli nuovi quelli che gia' ci sono 
			logger.debug('dict_from_file : ' + str(dict_from_file))
			dict_result_tags = {}

			for key,value in dict_from_file.items():
				for __tag in value:
					if key in old_tags and __tag in old_tags[ key ]:
						continue

					if key in dict_result_tags:
						dict_result_tags[key].append( __tag )
					else:
						dict_result_tags[key] = [ __tag ]

			logger.debug('dict_result_tags : ' + str(dict_result_tags))
			for __topic,value in dict_result_tags.items():
				for tag in value:
					__payload = ET.SubElement( __list, 'vdf:payload')
					__tag = ET.SubElement( __payload, 'vdf:field')
					__tag.set('name','tag')
					__origin = ET.SubElement( __tag, 'vdf:origin')
					__origin.set('href', os.environ['CUE_TAG_URL'] + __topic + ',' + tag )
					# qui non so dove prendere il value - per es "Sentimentale"
					__relevance = ET.SubElement( __payload, 'vdf:field')
					__relevance.set('name','relevance')
					__value = ET.SubElement( __relevance, 'vdf:value')
					__value.text = "1"



	def createTags(self):
		logger.debug(' INIT createTags')
		# da verificare se lasciare solo __TAGS__ ... CLAD DEBUG
		if '__TAGS_MAMPROGRAMMEVIDEO__' in self.assetdata and len(self.assetdata['__TAGS_MAMPROGRAMMEVIDEO__']) >0:
			__fieldTag = ET.SubElement( self.payload, 'vdf:field')
			__fieldTag.set('name','com.escenic.tags')
			__list = ET.SubElement( __fieldTag, 'vdf:list')
			
			for tag in self.assetdata['__TAGS_MAMPROGRAMMEVIDEO__']:

				__payload = ET.SubElement( __list, 'vdf:payload')
				__tag = ET.SubElement( __payload, 'vdf:field')
				__tag.set('name','tag')
				__origin = ET.SubElement( __tag, 'vdf:origin')
				__origin.set('href', os.environ['CUE_TAG_URL'] + 'tag:srg.topic.rsi.ch,' + tag )
				# qui non so dove prendere il value - per es "Sentimentale"
				__relevance = ET.SubElement( __payload, 'vdf:field')
				__relevance.set('name','relevance')
				__value = ET.SubElement( __relevance, 'vdf:value')
	
				__payload = ET.SubElement( __list, 'vdf:payload')
				__tag = ET.SubElement( __payload, 'vdf:field')
				__tag.set('name','tag')
				__origin = ET.SubElement( __tag, 'vdf:origin')
				__origin.set('href', os.environ['CUE_TAG_URL'] + 'tag:hbbtv.topic.rsi.ch,' + tag )
				# qui non so dove prendere il value - per es "Sentimentale"
				__relevance = ET.SubElement( __payload, 'vdf:field')
				__relevance.set('name','relevance')
				__value = ET.SubElement( __relevance, 'vdf:value')
				__value.text = "1"

	
	def addSegmentOrder(self, segmentId , order):
		
		logger.debug ( float(order ))
		# prendo la lista dei related
		_linkSegment = self.creaRelationSegment( segmentId, order )
		#_thumbnailLink = self.creaRelationThumbnail( keyframeId )
		listaSegments = self.prendiListaSegments()
		logger.debug(len(listaSegments))
		listaSegments.append( _linkSegment )
		self.rimuoviListaSegments()
		self.aggiungiSegmentiOrdinati(listaSegments)


	def prendiListaEditorialKeyframes(self):

		result = []
		list =  self.root.findall(namespaces['atom'] + "link")
		for idx , lis in enumerate(list):
			#logger.debug(idx, lis)
			logger.debug(lis.attrib)
			if namespaces['metadata']+ 'group' in lis.attrib:
				if "editorialkeyframes" in lis.attrib[namespaces['metadata'] + 'group']:
					result.append( lis )
		return result


	def prendiListaKeyframes(self):

		result = []
		list =  self.root.findall(namespaces['atom'] + "link")
		for idx , lis in enumerate(list):
			#logger.debug(idx, lis)
			logger.debug(lis.attrib)
			if namespaces['metadata']+ 'group' in lis.attrib:
				if "editorialkeyframes" in lis.attrib[namespaces['metadata'] + 'group']:
					continue
				if "keyframes" in lis.attrib[namespaces['metadata'] + 'group']:
					result.append( lis )
		return result

	def esisteEditorialKeyframeTitle( self, title ):
		result = False
		link = self.prendiListaEditorialKeyframes()
		for key in link:
			if title in key.attrib['title']:
				logger.debug("trovato titolo")
				return True

		return result


	def esisteKeyframeTitle( self, title ):
		result = False
		link = self.prendiListaKeyframes()
		for key in link:
			if title in key.attrib['title']:
				logger.debug("trovato titolo")
				return True

		return result

			
	def addRelKeyframe(self, keyframeId, editorial ):
		# prendo la lista dei related
		_linkKeyframe = self.creaRelationKeyframe( keyframeId, editorial )
		#_thumbnailLink = self.creaRelationThumbnail( keyframeId )
		listaRelated = self.prendiListaRelated("related")
		self.rimuoviListaRelated("related")
		self.aggiungiEditorialList(_linkKeyframe, listaRelated)

	def preparaKeyframesProgramme( self ):
		# qui in self.assetdata sono sicuro di trovare self.assetdata['message']['transcoderMetadata']
		# perche' altimenti non sareiu arrivato a questa funzione

		logger.debug ( '------------------------ INIT  preparaKeyframesProgrammeContentType -------------- ' )
		logger.debug ( '------------------------ INIT  preparaKeyframesProgrammeContentType -------------- ' )
		logger.debug( self.assetdata )
		if 'transcoderMetadata' in self.assetdata['message']:
			logger.debug('transcoderMetadata existent')
			awsJson = self.assetdata['message']['transcoderMetadata']
		else:
			logger.debug ('passo da resultBool == FALSE ' )
			logger.debug('transcoderMetadata not existent')
			return None
		result = ''

		if 'urn' in self.assetdata['message']:
			name = self.assetdata['message']['urn']
		elif 'mamUrn' in self.assetdata['message']:
			 name = self.assetdata['message']['mamUrn']

		if 'keyFrames'in awsJson and not(awsJson['keyFrames'] is None) and len( awsJson['keyFrames'] ) > 0:
			# devi creare i keyframe nella sezione giusta
			logger.debug ( 'prendo : ' + str(awsJson['keyFrames'] ) )
			logger.debug ( 'prendo : ' + str(awsJson['keyFrames'] ))
			for kf in awsJson['keyFrames']:
				# kf e nella forma :
				#{
				#  "timestamp":"timestamp1",
				#	  "url" : "imageS3Url1"
				#}

				# prendo la immagine da  S3
				kUrl = kf['url']
				kTitle = str(kf['timestamp']) + '_' + name
				logger.debug ('title = ' + kTitle )
				resultBool = False
				cueId = -1
				[ resultBool, cueId ] = pyTools.importaImgFromAws( kUrl, self.assetdata['section'], kTitle )

				if not resultBool:
					logger.debug ('passo da resultBool == FALSE ' )
					return None

				# con l'immagine appena creata devo andare a metterla nelle ralazioni del capo
				if ( '__IF_EDITORIAL__' in self.assetdata and self.assetdata['__IF_EDITORIAL__'] ) or 'editorialKeyframe' in self.assetdata:
					editorial = 'editorialkeyframes'
				else:
					editorial = 'keyframes'

				self.addRelKeyframe( cueId, editorial )	


		logger.debug ( '------------------------ END  preparaKeyframesProgramme -------------- ' )
		logger.debug ( '------------------------ END  preparaKeyframesProgramme -------------- ' )

class Story(ContentType):
	def __init__(self):
		super().__init__()
		self.model = 'story'
		logger.debug('sono un story')
		#self.initMap()

	def createDocument(self):
		super().createDocument()
		self.payload.set( 'model', os.environ['CUE_CONTENTTYPE'] + 'story')

class Gallery(ContentType):
	def __init__(self):
		super().__init__()
		self.model = 'gallery'
		logger.debug('sono un gallery')
		#self.initMap()

	def createDocument(self):
		super().createDocument()
		self.payload.set( 'model', os.environ['CUE_CONTENTTYPE'] + 'gallery')




class Recipe(ContentType):
	def __init__(self):
		super().__init__()
		self.model = 'recipe'
		logger.debug('sono un recipe')
		#self.initMap()

	def createDocument(self):
		super().createDocument()
		self.payload.set( 'model', os.environ['CUE_CONTENTTYPE'] + 'recipe')






class Series(ContentType):
	def __init__(self):
		super().__init__()
		self.model = 'series'
		logger.debug('sono un series')
		#self.initMap()

	def createDocument(self):
		super().createDocument()
		self.payload.set( 'model', os.environ['CUE_CONTENTTYPE'] + 'series')



	
class Keyframe(ContentType):

	def __init__(self):
		super().__init__()
		logger.debug('sono un keyframe')
		self.model = 'picture'
		
		self.initMap()

	def createDocument(self):
		super().createDocument()
		self.payload.set( 'model', os.environ['CUE_CONTENTTYPE'] + 'picture')
		

	def initMap(self):
		# questa non fa nulla 
		# ma negli altri ci sara' la vecchia listaFields
		 self.listaFields = {'title':'title'}

	def copyRelations(self):
		# sistema le reazioni lead e related
		logger.debug('copyRelations di keyframe')
		return

	def sistemaBinary(self, binary):
		# questa crea la entry per il binary 
		# solo per pictures
		__field = self.prendiField( 'binary' )
		if __field is None:
			# allora lo creo e poi gli setto il valore
			__field = ET.SubElement(self.payload, 'vdf:field')
			__field.set('name', 'binary' )
			__fieldValue = ET.SubElement(__field, 'vdf:value')
			__link = ET.SubElement(__fieldValue, 'link')
			__link.set( 'rel','edit-media' )
			__link.set( 'type', 'image/jpeg')
			__link.set( 'href', binary )
			__link.set( 'title', self.assetdata['title'] )
		else:
			__fieldValue = __field.find( 'vdf:value' )
			__link = __fieldValue.find( 'link' )
			__link.set( 'href', binary )
			__link.set( 'title', self.assetdata['title'] )
			
			
		return

class ProgrammeVideo(ContentType):

	def __init__(self):
		super().__init__()
		logger.debug('sono un PV')
		self.model = 'video'
		self.initMap()

	def createDocument(self):
		super().createDocument()
		self.payload.set( 'model', os.environ['CUE_CONTENTTYPE'] + 'video')
		

	def initMap(self):
		# questa non fa nulla 
		# ma negli altri ci sara' la vecchia listaFields
		 self.listaFields = {
			"title":"title",
			"editorialContent_titlePress":"title",
			"editorialContent_shortDescriptionPress":"subtitle",
			"dateTimes_startBroadcastPress" : "startTime",
			"editorialContent_longDescriptionPress" : "body",
			"channel":"channel",
			"editorialContent_show_title":"parentSeries",
			"editorialContent_episodeNr":"episodeNumber",
			"editorialContent_productionYear":"productionYear",

			"sourceSystem_louise_replica":"replica",
			"features_audioDoubleChannel":"flagbicanale",
			"features_signLanguage":"flagsignlanguage",
			"features_txtSubtitles":"flagteletext",
			"sourceSystem_maxResolution":"maxresolution",
			"editorialContent_warningDescription":"adultwarning",
			"sourceSystem_urn":"mpUrn",



			"cms_urn" : "programmeId",
			"cms_louise" : "ProductId",
			"sourceSystem_louise_urn" : "ProductId",
			"rights_geoblocked":"geoBlocked",
			"geoBlocked":"geoBlocked",
			"mediaexpiredate":"mediaexpiredate",
			"duration":"duration",
			"QoS":"qos",
			"logo":"logo",
			"urn":"mamUrn",
			"mamUrn":"mamUrn",
			"productId":"ProductId",
			"dateTimes_startBroadcastPress":"pubdate",
			"pubdate":"pubdate",
			"subtitleUrl":"subtitleUrl",
			"clips_markIn":"startTimeInMs",
			"transcoderMetadata":"transcoderMetadata",
			"status":"transcoderMamStatus",
			"transcoderMamStatus":"transcoderMamStatus",
			"editorialtype":"editorialtype",
			"binaryPath":"binary"
			#"__TAGS_MAMPROGRAMMEVIDEO__" : "__TAGS_MAMPROGRAMMEVIDEO__",
			#"__ECE_LINK_KEYFRAME__":"__ECE_LINK_KEYFRAME__"
		}
		# message - CUE
		 self.listaUpdateFields = {
			"channel":"channel",
			"programmeId":"programmeId",
			"productId":"ProductId",
			"geoblocked":"geoBlocked",
			"duration":"duration",
			"QoS":"qos",
			"logo":"logo",
			"urn":"mamUrn",
			"mamUrn":"mamUrn",
			"playMarkIn":"playMarkIn",		
			"clips_markIn":"startTimeInMs",
			"dateTimes_startBroadcastPress":"pubdate",
			"pubdate":"pubdate",
			"drm":"drm",
			"drmstatus":"drmstatus",
			"subtitleUrl":"subtitleUrl",
			"status":"transcoderMamStatus",
			"transcoderMetadata":"transcoderMetadata",
			"transcoderMamStatus":"transcoderMamStatus",
		}

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

		tmpVal = self.prendiFieldValue('channel')
			
		if tmpVal is None or len(tmpVal) < 1:
			logger.debug( "ritorno -1 perche tmpVal CHANNEL e nullo")
			logger.warning( "ritorno -1 perche tmpVal CHANNEL e nullo")
			jsonForSection['channel'] = ''
		else:
			jsonForSection['channel'] = tmpVal

		tmpVal = self.prendiFieldValue( 'parentSeries')
		if tmpVal is None or len(tmpVal) < 1:
			logger.debug( "ritorno a prendere il valore dal link della homesection perche tmpVal PARENTSERIES era nullo")
			logger.debug( "ritorno a prendere il valore dal link della homesection perche tmpVal PARENTSERIES era nullo")
			# non devo tornare bensi usare il metodo vecchio 
			# ed andare a prenderlo dal link con home-section
			return self.prendiHomeSectionDaProgramme( )
		else:
			jsonForSection['__DA_PASSARE_A_BRAND__'] = tmpVal

		'''
		tmpVal = self.prendiField( 'episode_producttypedesc')
		if not (tmpVal is None ) and len(tmpVal) > 1:
			# questo non e' indispensabile
			# quindi se non c'e' non importa
			jsonForSection['__PRODUCTTYPEDESC_MAMPROGRAMME__'] = tmpVal

		'''
		result = pyTools.prendiSectionId(jsonForSection)

		logger.debug( '------------------------ END prendiSectionDaProgramme -------------- ' )
		logger.debug( '------------------------ END prendiSectionDaProgramme -------------- ' )
		return result
			

	def copyRelations(self):
		# sistema le reazioni lead e related
		logger.debug('copyRelations di keyframe')
		return

	def preparaKeyframesProgramme( self ):
		# qui in self.assetdata sono sicuro di trovare self.assetdata['message']['transcoderMetadata']
		# perche' altimenti non sareiu arrivato a questa funzione
		logger.debug ( '------------------------ INIT  preparaKeyframesProgrammeVideo -------------- ' )
		logger.debug ( '------------------------ INIT  preparaKeyframesProgrammeVideo -------------- ' )
		
		if 'transcoderMetadata' in self.assetdata['message']:
			logger.debug('transcoderMetadata existent')
			awsJson = self.assetdata['message']['transcoderMetadata']
		else:
			logger.debug ('passo da resultBool == FALSE ' )
			logger.debug('transcoderMetadata not existent')
			return None
		result = ''
		name = ''

		if 'urn' in self.assetdata['message']:
			name = self.assetdata['message']['urn']
		elif 'mamUrn' in self.assetdata['message']:
			name = self.assetdata['message']['mamUrn']
		elif 'transcoderMetadata' in self.assetdata['message'] and  'urn' in self.assetdata['message'][ 'transcoderMetadata']:
			name = self.assetdata['message'][ 'transcoderMetadata']['urn']
		elif 'cms_asset_urn' in self.assetdata:
			name = self.assetdata['cms_asset_urn']

		logger.debug(name)

		if 'keyFrames'in awsJson and not(awsJson['keyFrames'] is None) and len( awsJson['keyFrames'] ) > 0:
			# devi creare i keyframe nella sezione giusta
			logger.debug ( 'prendo : ' + str(awsJson['keyFrames'] ) )
			logger.debug ( 'prendo : ' + str(awsJson['keyFrames'] ))
			for kf in awsJson['keyFrames']:
				# kf e nella forma :
				#{
				#  "timestamp":"timestamp1",
				#	  "url" : "imageS3Url1"
				#}

				# prendo la immagine da  S3
				kUrl = kf['url']
				
				timestamp = str(kf['timestamp'])
				#kTitle = str(kf['timestamp']) + '_' + name
				name = name.split(':')[-1]
				kTitle =  timestamp + '_' + name
				logger.debug ('title = ' + kTitle )
				resultBool = False
				cueId = -1
				# qui prima di importarla e crearne una nuova devo
				# verificare che con quel titolo non ce ne sia gia' una attaccata ....
				if self.esisteKeyframeTitle( kTitle ):
					logger.debug("Esiste gia il keyframe con title: " + kTitle )
					continue
				[ resultBool, cueId ] = pyTools.importaImgFromAws( kUrl, self.assetdata['section'], kTitle )

				if not resultBool:
					logger.debug ('passo da resultBool == FALSE ' )
					return ''

				# con l'immagine appena creata devo andare a metterla nelle ralazioni del capo
				if ( '__IF_EDITORIAL__' in self.assetdata and self.assetdata['__IF_EDITORIAL__'] ) or 'editorialKeyframe' in self.assetdata:
					editorial = 'editorialkeyframes'
				else:
					editorial = 'keyframes'

				self.addRelKeyframe( cueId, editorial )	


		logger.debug ( '------------------------ END  preparaKeyframesProgramme -------------- ' )
		logger.debug ( '------------------------ END  preparaKeyframesProgramme -------------- ' )
		
	def cambiatoStartTimeInMs( self, listaToUpdate ):

		logger.debug('------------------------ INIT cambiatoStartTimeInMs  -------------- ' )     
		
		if not 'startTimeInMs' in listaToUpdate:
			logger.debug(' startTimeInMs not in listaToUpdate !!!! ESCO ' )
			logger.debug('------------------------ END cambiatoStartTimeInMs  -------------- ' )     
			return False

		else:
			# ne prendo il valore e verifico se e uguale a quello 
			# pre esistente
			local_stInMs = self.prendiFieldValue('startTimeInMs')
			logger.debug(local_stInMs)
			if local_stInMs is None:
				return True
			local_stInMs = float(local_stInMs)
			new_stInMs = float(listaToUpdate['startTimeInMs'])
			logger.debug(local_stInMs)
			logger.debug(new_stInMs)
			if local_stInMs == new_stInMs:
				logger.debug('trovati uguali -> non fare una ceppa')
				return False
			else:
				logger.debug('trovati diversi -> cambia offset ')
				return True

		logger.debug('------------------------ END cambiatoStartTimeInMs  -------------- ' )     
		return False

	def sistema_offset_pubdate_segments( self, startTimeInMs, pubdate ):

		logger.debug('------------------------ INIT sistema_offset_pubdate_segments  -------------- ' )     
		# per tutti i segmenti vado a sistemare gli offset giusti
		listaSegments = self.prendiListaSegmentsId()
		#logger.debug('listaSegments : ' + str(listaSegments))
		#logger.debug('len listaSegments : ' + str(len(listaSegments)))

		# in listaSegments ho la lista degli id
		for lis in listaSegments:
			logger.debug('aggiorno offset segmento : ' + str(lis))
			
			successGetId = -1
			[ successGetId, updateSv  ] = MasterType(  lis, None, None )
			updateSv.aggiornaOffset( startTimeInMs )
			stato = updateSv.getState()
			updateSv.cambiaState(stato)
			# e aggiorno anche la pubdate
			updateSv.addUpdateVdfField( 'pubdate', pubdate )
			
			resultBool = False
			resultBool = updateSv.putToCue()
		
		# lo prendo e gli chiamo sopra la setOffset con il valore del startTimeInMs appena preso
		logger.debug('------------------------ END sistema_offset_pubdate_segments  -------------- ' )     
		return



	def sistemaOffsetSegments( self, startTimeInMs ):
		# OLD version deprecata
		logger.debug('------ DEPRECATED -------------- INIT sistemaOffsetSegments  -------------- ' )     
		logger.warning('------ DEPRECATED -------------- INIT sistemaOffsetSegments  -------------- ' )     
		'''
		
		# per tutti i segmenti vado a sistemare gli offset giusti
		listaSegments = self.prendiListaSegmentsId()
		#logger.debug('listaSegments : ' + str(listaSegments))
		#logger.debug('len listaSegments : ' + str(len(listaSegments)))

		# in listaSegments ho la lista degli id
		for lis in listaSegments:
			logger.debug('aggiorno offset segmento : ' + str(lis))
			
			successGetId = -1
			[ successGetId, updateSv  ] = MasterType(  lis, None, None )
			updateSv.aggiornaOffset( startTimeInMs )
			stato = updateSv.getState()
			updateSv.cambiaState(stato)
			resultBool = False
			resultBool = updateSv.putToCue()
		
		# lo prendo e gli chiamo sopra la setOffset con il valore del startTimeInMs appena preso
		'''
		logger.debug('------------------------ END sistemaOffsetSegments  -------------- ' )     
		return


class VideoSegment(ContentType):

	def __init__(self):
		super().__init__()
		logger.debug('sono un SV')
		self.model = 'videosegment'
		self.initMap()

	def createDocument(self):
		super().createDocument()
		self.payload.set( 'model', os.environ['CUE_CONTENTTYPE'] + 'videosegment')
		

	def initMap(self):
		# questa non fa nulla 
		# ma negli altri ci sara' la vecchia listaFields

		 self.listaFields = {
			"title":"title",
			"tc_offset":"offset",
			"clips_markIn":"clipsMarkIn",
			"duration":"duration",
			"QoS":"qos",
			"logo":"logo",
			"channel":"channel",
			"mamUrn":"mamUrn",
			"programmeVideoId":"parentId",
			"geoblocked":"geoBlocked",
			"geoBlocked":"geoBlocked",
			"mediaactivedate" : "mediaactivedate",
			"mediaexpiredate" : "mediaexpiredate"
			#"cms_urn" : "__PROGRAMMEID_MAMSEGMENTVIDEO__",
			#"rights_expireDate":"rights_expireDate",
			#"rights_activationDate" : "rights_activationDate",
			#"transcoderMetadata":"__TRANSCODERMETADATA_MAMSEGMENTVIDEO__",
			#"status":"__TRANSCODERMAMSTATUS_MAMSEGMENTVIDEO__",
			#"state":"state",
			#"__ECE_UPDATED__" : "__ECE_UPDATED__",
			#"__ECE_AGE_EXPIRES__":"__ECE_AGE_EXPIRES__",
			#"__ECE_DCTERMS_AVAILABLE__":"__ECE_DCTERMS_AVAILABLE__",
			#"__ECE_LINK_KEYFRAME__":"__ECE_LINK_KEYFRAME__"
			}

		 self.listaUpdateFields = {
			"title":"title",
			"tc_offset":"offset",
			"clips_markIn":"clipsMarkIn",
			"duration":"duration",
			"QoS":"qos",
			"logo":"logo",
			"channel":"channel",
			"mamUrn":"mamUrn",
			"programmeVideoId":"parentId",
			"geoblocked":"geoBlocked",
			"mediaactivedate" : "mediaactivedate",
			"mediaexpiredate" : "mediaexpiredate"
			#"cms_urn" : "__PROGRAMMEID_MAMSEGMENTVIDEO__",
			#"rights_expireDate":"rights_expireDate",
			#"rights_activationDate" : "rights_activationDate",
			#"transcoderMetadata":"__TRANSCODERMETADATA_MAMSEGMENTVIDEO__",
			#"status":"__TRANSCODERMAMSTATUS_MAMSEGMENTVIDEO__",
			#"state":"state",
			#"__ECE_UPDATED__" : "__ECE_UPDATED__",
			#"__ECE_AGE_EXPIRES__":"__ECE_AGE_EXPIRES__",
			#"__ECE_DCTERMS_AVAILABLE__":"__ECE_DCTERMS_AVAILABLE__",
			#"__ECE_LINK_KEYFRAME__":"__ECE_LINK_KEYFRAME__"
			}


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

		tmpVal = self.prendiFieldValue('channel')
			
		if tmpVal is None or len(tmpVal) < 1:
			logger.debug( "ritorno -1 perche tmpVal CHANNEL e nullo")
			logger.warning( "ritorno -1 perche tmpVal CHANNEL e nullo")
			jsonForSection['channel'] = ''
		else:
			jsonForSection['channel'] = tmpVal

		tmpVal = self.prendiFieldValue( 'parentSeries')
		if tmpVal is None or len(tmpVal) < 1:
			logger.debug( "ritorno a prendere il valore dal link della homesection perche tmpVal PARENTSERIES era nullo")
			logger.debug( "ritorno a prendere il valore dal link della homesection perche tmpVal PARENTSERIES era nullo")
			# non devo tornare bensi usare il metodo vecchio 
			# ed andare a prenderlo dal link con home-section
			return self.prendiHomeSectionDaProgramme( )
		else:
			jsonForSection['__DA_PASSARE_A_BRAND__'] = tmpVal

		'''
		tmpVal = self.prendiField( 'episode_producttypedesc')
		if not (tmpVal is None ) and len(tmpVal) > 1:
			# questo non e' indispensabile
			# quindi se non c'e' non importa
			jsonForSection['__PRODUCTTYPEDESC_MAMPROGRAMME__'] = tmpVal

		'''
		result = pyTools.prendiSectionId(jsonForSection)

		logger.debug( '------------------------ END prendiSectionDaProgramme -------------- ' )
		logger.debug( '------------------------ END prendiSectionDaProgramme -------------- ' )
		return result
			

	def creaRelationVideoPrincipale(self, videoId ):
		__link = ET.SubElement(self.root, 'link')
		__link.set('href',os.environ['CUE_CONTENT'] + videoId)
		__link.set('xmlns:vaext','http://www.vizrt.com/atom-ext')
		__link.set('xmlns:vdf','http://www.vizrt.com/types')
		__link.set('rel','related')
		__link.set('title','') 
		__link.set('type','application/atom+xml; type=entry')
		__link.set('dcterms:identifier',videoId)	
		__link.set('metadata:group',"parent" )
		__link.set('metadata:synthetic-id','')
		__link.set('vaext:state','published')
		__payload = ET.SubElement( __link, 'vdf:payload')
		__payload.set('model',os.environ['CUE_CONTENTSUMMARY'] + 'video' )
		#__caption = ET.SubElement( __payload, 'vdf:field')
		#__caption.set('name','caption')
		#__credits = ET.SubElement( __payload, 'vdf:field')
		#__credits.set('name','credits')
		#__crop = ET.SubElement( __payload, 'vdf:field')
		#__crop.set('name','crop')
		#__value = ET.SubElement( __crop, 'vdf:value')
		#__value.text = 'r16x9'

	def copyRelations(self):
		# sistema le reazioni lead e related
		logger.debug('copyRelations di keyframe')
		return


	def preparaKeyframesSegmentedVideo( self ):
		# qui in self.assetdata sono sicuro di trovare self.assetdata['message']['transcoderMetadata']
		# perche' altimenti non sareiu arrivato a questa funzione
		logger.debug ( '------------------------ INIT  preparaKeyframesSegmentedVideo -------------- ' )
		logger.debug ( '------------------------ INIT  preparaKeyframesSegmentedVideo -------------- ' )

		logger.debug(self.assetdata)
		if 'awsKeyframe_status' not in self.assetdata or not 'SUCCEEDED' in self.assetdata['awsKeyframe_status']:
			return result	

		result = ''
		if 'awsKeyframe_url'in self.assetdata and not(self.assetdata['awsKeyframe_url'] is None )and len( self.assetdata['awsKeyframe_url'] ) > 0:
			# devi creare i keyframe nella sezione giusta
			logger.debug ( 'prendo : ' + str(self.assetdata['awsKeyframe_url'] ) )
			logger.debug ( 'prendo : ' + str(self.assetdata['awsKeyframe_url'] ))

			# prendo la immagine da  S3
			kUrl = self.assetdata['awsKeyframe_url']
			timestampJpg = kUrl.split('/')[-1]
			timestamp = timestampJpg.replace('.jpg','').replace('.JPG','')
			# se il timestamp e gia' presente nella lista non lo creo ne' importo
			# altrimenti proseguo
			if ( pyTools.esisteTimeStamp( self.assetdata, timestamp )):
				return ''
			kTitle = timestamp + '_' + self.assetdata['urn']
			logger.debug ('title = ' + kTitle )
			resultBool = False
			cueId = -1
			if self.esisteKeyframeTitle( kTitle ):
				logger.debug("Esiste gia il keyframe con title: " + kTitle )
				return ''
			[ resultBool, cueId ] = pyTools.importaImgFromAws( kUrl, self.assetdata['section'], kTitle )

			if not resultBool:
				logger.debug ('passo da resultBool == FALSE ' )
				return ''

			# con l'immagine appena creata devo andare a metterla nelle ralazioni del capo
			if ( '__IF_EDITORIAL__' in self.assetdata and self.assetdata['__IF_EDITORIAL__'] ) or 'editorialKeyframe' in self.assetdata:
				editorial = 'editorialkeyframes'
			else:
				editorial = 'keyframes'
				
			self.addRelKeyframe( cueId, editorial )	


		logger.debug ( '------------------------ END  newSv.preparaKeyframesSegmentedVideo -------------- ' )
		logger.debug ( '------------------------ END  newSv.preparaKeyframesSegmentedVideo -------------- ' )

	
	def aggiornaOffset( self,startTimeInMs ):
		logger.debug( '------------------------ INIT aggiornaOffset ----------------')
		local_clMkIn = self.prendiFieldValue('clipsMarkIn')
		nuovo_offset = float(local_clMkIn) - float(startTimeInMs)
		self.addUpdateVdfField( 'offset', str(nuovo_offset ))

		logger.debug( '------------------------ END aggiornaOffset ----------------')

class TranscodableVideo(ProgrammeVideo):
	def __init__(self):
		super().__init__()
		self.model = 'video'
		logger.debug('sono un TranscodableVideo')

class Video(ProgrammeVideo):
	def __init__(self):
		super().__init__()
		self.model = 'video'
		logger.debug('sono un Video')

class VideoProgramme(ProgrammeVideo):
	def __init__(self):
		super().__init__()
		self.model = 'video'
		logger.debug('sono un VideoProgramme')

	def initMap(self):

		self.listaFields = {

		"editorialContent_titlePress":"title",
		"editorialContent_shortDescriptionPress":"subtitle",
		"dateTimes_startBroadcastPress" : "startTime",
		"editorialContent_longDescriptionPress" : "body",
		"channel":"channel",
		"editorialContent_show_title":"parentSeries",
		"editorialContent_episodeNr":"episodeNumber",
		"editorialContent_productionYear":"productionYear",

		#"sourceSystem_louise_productTypeDescription":"__PRODUCTTYPEDESC_MAMPROGRAMME__",
		#"sourceSystem_lastupdate":"__LASTUPDATE_MAMPROGRAMME__",
		#"sourceSystem_louise_primeur":"__PRIMEUR_MAMPROGRAMME__",

		"sourceSystem_louise_replica":"replica",
		"features_audioDoubleChannel":"flagbicanale",
		"features_signLanguage":"flagsignlanguage",
		"features_txtSubtitles":"flagteletext",
		"sourceSystem_maxResolution":"maxresolution",
		"editorialContent_warningDescription":"adultwarning",

		#"duration":"duration",
		"urn":"mamUrn",
		"mamUrn":"mamUrn",
		"QoS":"qos",
		"transcoderMamStatus":"transcoderMamStatus",
		"sharedcontentstatus":"sharedcontentstatus",
		"lanostrastoriastatus":"lanostrastoriastatus",
		#"sourceSystem_louise_urn":"__LOUISEURN_MAMPROGRAMME__",
		"rights_geoblocked":"geoBlocked",
		"geoblocked":"geoBlocked",
		"geoBlocked":"geoBlocked",
		"sourceSystem_urn":"mpUrn",

		}

		self.listaUpdateFields = {
		#"editorialContent_titlePress":"title",
		#"editorialContent_shortDescriptionPress":"subtitle",
		"dateTimes_startBroadcastPress" : "startTime",
		#"editorialContent_longDescriptionPress" : "body",
		"channel":"channel",
		"editorialContent_show_title":"parentSeries",
		"editorialContent_episodeNr":"episodeNumber",
		"editorialContent_productionYear":"productionYear",
		"editorialtype":"editorialtype",
		#"sourceSystem_louise_productTypeDescription":"__PRODUCTTYPEDESC_MAMPROGRAMME__",
		#"sourceSystem_lastupdate":"__LASTUPDATE_MAMPROGRAMME__",
		#"sourceSystem_louise_primeur":"__PRIMEUR_MAMPROGRAMME__",
		"sourceSystem_louise_replica":"replica",
		"features_audioDoubleChannel":"flagbicanale",
		"features_signLanguage":"flagsignlanguage",
		"features_txtSubtitles":"flagteletext",
		"sourceSystem_maxResolution":"maxresolution",
		"editorialContent_warningDescription":"adultwarning",
		#"duration":"duration",
		"urn":"mamUrn",
		"mamUrn":"mamUrn",
		"QoS":"qos",
		"transcoderMamStatus":"transcoderMamStatus",
		"transcoderMetadata":"transcoderMetadata",
		"sharedcontentstatus":"sharedcontentstatus",
		"lanostrastoriastatus":"lanostrastoriastatus",
		#"sourceSystem_louise_urn":"__LOUISEURN_MAMPROGRAMME__",
		"rights_geoblocked":"geoBlocked",
		"geoblocked":"geoBlocked",
		"geoBlocked":"geoBlocked",
		#"sourceSystem_urn":"__MPURN_MAMPROGRAMME__",
		}






class ProgrammeAudio(ContentType):

	def __init__(self):
		super().__init__()
		logger.debug('sono un PA')
		self.model = 'audio'
		self.initMap()

	def createDocument(self):
		super().createDocument()
		self.payload.set( 'model', os.environ['CUE_CONTENTTYPE'] + 'audio')
		

	def initMap(self):

		self.listaFields = {
		"title":"title",
		"editorialContent_titlePress":"title",
		"editorialContent_shortDescriptionPress":"subtitle",
		"dateTimes_startBroadcastPress" : "startTime",
		"editorialContent_longDescriptionPress" : "body",
		"channel":"channel",
		"editorialContent_show_title":"parentSeries",
		"editorialContent_episodeNr":"episodeNumber",
		"editorialContent_productionYear":"productionYear",
		#"sourceSystem_louise_productTypeDescription":"__PRODUCTTYPEDESC_MAMPROGRAMME__",
		#"sourceSystem_lastupdate":"__LASTUPDATE_MAMPROGRAMME__",
		#"sourceSystem_louise_primeur":"__PRIMEUR_MAMPROGRAMME__",
		"sourceSystem_louise_replica":"replica",
		"features_audioDoubleChannel":"flagbicanale",
		"features_signLanguage":"flagsignlanguage",
		"features_txtSubtitles":"flagteletext",
		"sourceSystem_maxResolution":"maxresolution",
		"editorialContent_warningDescription":"adultwarning",
		#"duration":"duration",
		"urn":"mamUrn",
		"mamUrn":"mamUrn",
		"QoS":"qos",
		"transcoderMetadata":"transcoderMetadata",
		"status":"transcoderMamStatus",
		#"sourceSystem_louise_urn":"__LOUISEURN_MAMPROGRAMME__",
		"rights_geoblocked":"geoBlocked",
		"geoBlocked":"geoBlocked",
		"sourceSystem_urn":"mpUrn",
		}

		self.listaUpdateFields = {
		#"editorialContent_titlePress":"title",
		#"editorialContent_shortDescriptionPress":"subtitle",
		"dateTimes_startBroadcastPress" : "startTime",
		#"editorialContent_longDescriptionPress" : "body",
		"channel":"channel",
		"editorialContent_show_title":"parentSeries",
		"editorialContent_episodeNr":"episodeNumber",
		"editorialContent_productionYear":"productionYear",
		"editorialtype":"editorialtype",
		#"sourceSystem_louise_productTypeDescription":"__PRODUCTTYPEDESC_MAMPROGRAMME__",
		#"sourceSystem_lastupdate":"__LASTUPDATE_MAMPROGRAMME__",
		#"sourceSystem_louise_primeur":"__PRIMEUR_MAMPROGRAMME__",
		"sourceSystem_louise_replica":"replica",
		"features_audioDoubleChannel":"flagbicanale",
		"features_signLanguage":"flagsignlanguage",
		"features_txtSubtitles":"flagteletext",
		"sourceSystem_maxResolution":"maxresolution",
		"editorialContent_warningDescription":"adultwarning",
		#"duration":"duration",
		"urn":"mamUrn",
		"mamUrn":"mamUrn",
		"QoS":"qos",
		"status":"transcoderMamStatus",
		"transcoderMamStatus":"transcoderMamStatus",
		"transcoderMetadata":"transcoderMetadata",
		#"sourceSystem_louise_urn":"__LOUISEURN_MAMPROGRAMME__",
		"rights_geoblocked":"geoBlocked",
		"geoBlocked":"geoBlocked",
		#"sourceSystem_urn":"__MPURN_MAMPROGRAMME__",
		}


class Audio(ProgrammeAudio):
	def __init__(self):
		super().__init__()
		self.model = 'audio'
		logger.debug('sono un Audio')


class AudioProgramme(ProgrammeAudio):
	def __init__(self):
		super().__init__()
		self.model = 'audio'
		logger.debug('sono un AudioProgramme')



class AudioSegment(ProgrammeAudio):
	def __init__(self):
		super().__init__()
		self.model = 'audiosegment'
		logger.debug('sono un AudioSegment')

	def createDocument(self):
		super().createDocument()
		self.payload.set( 'model', os.environ['CUE_CONTENTTYPE'] + 'audiosegment')

class Livestreaming(ContentType):
	def __init__(self):
		super().__init__()
		self.model = 'livestreaming'
		logger.debug('sono un livestreaming')
		self.initMap()

	def createDocument(self):
		super().createDocument()
		self.payload.set( 'model', os.environ['CUE_CONTENTTYPE'] + 'livestreaming')

	def initMap(self):

		self.listaFields = { 
		"title":"title", 
		"subtitle":"subtitle",
		"state":"state", # o arriva published ?
		"channel":"channel",
		"eventTime":"pubdate",
		"streamingStartTime":"startTime",
		"streamingEndTime":"endTime",
		"rsiProduzionePropria":"rsiProduction",
		"productId":"productId",
		"cesimId":"resultsCenterEventID",
		#"leadImageIdInEsc":"leadImageIdInEsc",
		"isWebOnly":"isWebOnly",
		"hasMusic":"containMusic",
		"rsiAuthor":"noRsiAuthor",
		"liveLinkId":"liveLinkId",
		"eventDescription":"event_description",
		#"regiaChannel":"__REGIACHANNEL_MAMLIVESTREAMING__",
		"eventnumber":"eventnumber",
		"eventType":"eventType",
		"eventGenre":"event_genre",
		"socialStart":"socialStartTime",
		"socialEnd":"socialEndTime",
		#"sectionIdInEsc":"__SECTIONIDINESC_MAMLIVESTREAMING__",

		#"cms_urn" : "__PROGRAMMEID_MAMLIVESTREAMING__",
		#"isGeoBlocked":"__ISGEOBLOCKED_MAMLIVESTREAMING__",
		"sportKey":"sportKey",
		#"hdn1URL":"__HDN1URL_MAMLIVESTREAMING__",
		#"hlsURL":"__HLSURL_MAMLIVESTREAMING__",
		#"hdsURL":"__HDSURL_MAMLIVESTREAMING__",

		"webActive":"webActive",
		"webVideoDesc":"webVideoDesc",
		"webVideoTitle":"webVideoTitle",
		"webencoder":"webencoder",
		"webisGeoBlocked":"webisGeoBlocked",
		"webuseOtherEncoder":"webuseOtherEncoder",
		"webextraStream":"webextraStream",
		"weblivesocialid":"weblivesocialid",
		"hbbtvActive":"hbbtvActive",
		"hbbtvVideoDesc":"hbbtvVideoDesc",
		"hbbtvVideoTitle":"hbbtvVideoTitle",
		"hbbtvencoder":"hbbtvencoder",
		"hbbtvisGeoBlocked":"hbbtvisGeoBlocked",
		"hbbtvlivesocialid":"hbbtvlivesocialid",

		#"mamUrn":"__MAMURN_MAMLIVESTREAMING__",
		"fblivesocencchan":"fblivesocencchan",
		"ioutubelivesocencchan":"ioutubelivesocencchan",
		#"__TAGS_MAMLIVESTREAMING__" : "__TAGS_MAMLIVESTREAMING__",
		#"__ECE_UPDATED__" : "__ECE_UPDATED__",
		#"__ECE_AGE_EXPIRES__":"__ECE_AGE_EXPIRES__",
		#"__ECE_DCTERMS_AVAILABLE__":"__ECE_DCTERMS_AVAILABLE__",
		#"__ECE_LINK_KEYFRAME__":"__ECE_LINK_KEYFRAME__"
		}



		self.listaUpdateFields = { 
		"state":"state", # o arriva published ?
		"channel":"channel",
		"eventTime":"eventTime",
		"streamingStartTime":"startTime",
		"streamingEndTime":"endTime",
		"rsiProduzionePropria":"rsiProduction",
		"productId":"productId",
		"cesimId":"resultsCenterEventID",
		#"leadImageIdInEsc":"leadImageIdInEsc",
		"isWebOnly":"isWebOnly",
		"hasMusic":"containMusic",
		"rsiAuthor":"noRsiAuthor",
		"liveLinkId":"liveLinkId",
		"eventDescription":"event_description",
		#"regiaChannel":"__REGIACHANNEL_MAMLIVESTREAMING__",
		"eventnumber":"eventnumber",
		"eventType":"eventType",
		"eventGenre":"event_genre",
		"socialStart":"socialStartTime",
		"socialEnd":"socialEndTime",
		#"sectionIdInEsc":"__SECTIONIDINESC_MAMLIVESTREAMING__",

		#"cms_urn" : "__PROGRAMMEID_MAMLIVESTREAMING__",
		#"isGeoBlocked":"__ISGEOBLOCKED_MAMLIVESTREAMING__",
		"sportKey":"sportKey",
		#"hdn1URL":"__HDN1URL_MAMLIVESTREAMING__",
		#"hlsURL":"__HLSURL_MAMLIVESTREAMING__",
		#"hdsURL":"__HDSURL_MAMLIVESTREAMING__",

		"webActive":"webActive",
		"webVideoDesc":"webVideoDesc",
		"webVideoTitle":"webVideoTitle",
		"webencoder":"webencoder",
		"webisGeoBlocked":"webisGeoBlocked",
		"webuseOtherEncoder":"webuseOtherEncoder",
		"webextraStream":"webextraStream",
		"weblivesocialid":"weblivesocialid",
		"hbbtvActive":"hbbtvActive",
		"hbbtvVideoDesc":"hbbtvVideoDesc",
		"hbbtvVideoTitle":"hbbtvVideoTitle",
		"hbbtvencoder":"hbbtvencoder",
		"hbbtvisGeoBlocked":"hbbtvisGeoBlocked",
		"hbbtvlivesocialid":"hbbtvlivesocialid",

		#"mamUrn":"__MAMURN_MAMLIVESTREAMING__",
		"fblivesocencchan":"fblivesocencchan",
		"ioutubelivesocencchan":"ioutubelivesocencchan",
		#"__TAGS_MAMLIVESTREAMING__" : "__TAGS_MAMLIVESTREAMING__",
		#"__ECE_UPDATED__" : "__ECE_UPDATED__",
		#"__ECE_AGE_EXPIRES__":"__ECE_AGE_EXPIRES__",
		#"__ECE_DCTERMS_AVAILABLE__":"__ECE_DCTERMS_AVAILABLE__",
		#"__ECE_LINK_KEYFRAME__":"__ECE_LINK_KEYFRAME__"
		}

	def preparaKeyframesLivestreaming( self ):
		# qui in self.assetdata sono sicuro di trovare self.assetdata['message']['transcoderMetadata']
		# perche' altimenti non sareiu arrivato a questa funzione
		logger.debug ( '------------------------ INIT  preparaKeyframesLivestreaming -------------- ' )
		logger.debug ( '------------------------ INIT  preparaKeyframesLivestreaming -------------- ' )

		logger.debug(self.assetdata)
		if 'leadImageIdInEsc' not in self.assetdata :
			logger.debug('non esiste leadImageIdInEsc ')
			return False	

		keyframeId = str(self.assetdata['leadImageIdInEsc'])

		# aggiunto per evitare errori ( solo in prod )
		# la verifica che il keyframeId esista
		resultBool = False
		[ resultBool, newL ] = MasterType( keyframeId, None, None )
		if not  resultBool:
			logger.debug('non trovo asset leadImageIdInEsc :' + keyframeId )
			return  False
		

		self.addRelKeyframe( keyframeId, 'lead' )	


		logger.debug ( '------------------------ END  newL.preparaKeyframesLivestreaming -------------- ' )
		logger.debug ( '------------------------ END  newL.preparaKeyframesLivestreaming -------------- ' )

	def sistemaSocials( self ) :

		#logger.debug(result)
		# devo girare sui channel e fare le cose opportune
		logger.debug ( '------------------------ INIT  sistemaSocials -------------- ' )

		logger.debug( self.assetdata)

		arr = []
		if 'socialChannels' in self.assetdata:
			arr = self.assetdata['socialChannels']
			logger.debug(arr)
		else:
			logger.debug('AGGIUNTO il 12.10.2023 ...... DEBUGGARE ! ')
			return	
		
		tmpFBresult = None
		tmpYTresult = None

		logger.debug ( sorted(arr,key = itemgetter('platformType'), reverse=True))

		# giro per i socialChannels e se 
		# se non esiste lo creo
		# se esiste lo lascio a meno che non sia una DELETE
		dict_channels = self.prendi_social_channels()
		
		for chan in self.assetdata['socialChannels']:
			if 'facebook' in chan['platformType'] or 'FB' in chan['platformType'] :
				# oppure se sono Social
				# devo creare la struttura Social opportuna
				logger.debug( chan['platformId'] )
				if str(chan['platformId'] ) in dict_channels:
					# esiste gia' non devo crearlo ...
					logger.debug(' channel con id : ' + str(chan['platformId'] ) + ' esiste gia non devo crearlo ..')
					logger.debug(' channel con id : ' + str(chan['platformId'] ) + ' esiste gia non devo crearlo ..')
					
					# e quindi lo lascio uguale mettendo il valore di dict_channels[ str(chan['platformId'] ) ]
					# nella lista che andro a riagganciare al payload

					tmpFBresult = self.copiaSocialXml(tmpFBresult,  dict_channels[ str(chan['platformId'] )])

					# verifico solo che non sia un delete 
					if chan['deletePlatform'] :
						logger.debug('devo cancellare il channel: ' + str(chan['platformId'] ))
					
					continue
	
				logger.debug( 'creo FB')
				# se platformType == facebook devo creare una entry nella lista
				# fblivesocencchan con il payload giusto
				tmpFBresult = self.creaSocialXml(tmpFBresult, chan, 'fblivesocencchan' )
				

			elif 'youtube' in chan['platformType'] or 'YOUTUBE' in chan['platformType'] :
				# se platformType == youtube  devo creare una entry nella lista
				# ioutubelivesocencchan con il payload giusto
				logger.debug( 'creo youtube')
		
				# ocio che va incapsulato nel caso sia una lista con piu elementi
				tmpYTresult = self.creaSocialXml(tmpYTresult, chan, 'ioutubelivesocencchan' )

		#self.dumpDoc()
		#exit(0)

				
		logger.debug ( '------------------------ MIDDLE  sistemaSocials -------------- ' )

		logger.debug(tmpFBresult)
		self.assetdata['fblivesocencchan'] = tmpFBresult
		self.assetdata['ioutubelivesocencchan'] = tmpYTresult

		if 'fblivesocencchan' in self.assetdata and not(self.assetdata['fblivesocencchan'] is None):
			# in self.assetdata['fblivesocencchan'] ho un element da inserire
			self.mettiNullaSocialList( 'fblivesocencchan')
			self.cambiaSocialList( 'fblivesocencchan', self.assetdata['fblivesocencchan']  )
		else:
			# devo aggiungere la lista nulla al nodo opportuno
			logger.debug('------------------------------------- passo da mettinulla')
			self.mettiNullaSocialList( 'fblivesocencchan')

		if 'ioutubelivesocencchan' in self.assetdata and not(self.assetdata['ioutubelivesocencchan'] is None):
			# in self.assetdata['fblivesocencchan'] ho un element da inserire
			self.mettiNullaSocialList(  'ioutubelivesocencchan')
			self.cambiaSocialList( 'ioutubelivesocencchan', self.assetdata['ioutubelivesocencchan']  )
		else:
			# devo aggiungere la lista nulla al nodo opportuno
			logger.debug('------------------------------------- passo da mettinulla')
			self.mettiNullaSocialList(  'ioutubelivesocencchan')

		if 'webextraStream' in  self.assetdata and not(self.assetdata['webextraStream'] is None):
			# in self.assetdata['fblivesocencchan'] ho un element da inserire
			nodo = self.creaExtraStreamXML( self.assetdata )
			self.mettiNullaSocialList(  'webextraStream')
			self.cambiaSocialList( 'webextraStream', nodo  )
		else:
			# devo aggiungere la lista nulla al nodo opportuno
			logger.debug('------------------------------------- passo da mettinulla')
			self.mettiNullaSocialList(  'webextraStream')

		
	def prendi_social_channels( self ):
		# devo fare la lista dei livesocialid aka platfomId
		#self.dumpDoc()
		logger.debug ( '------------------------ inizia prendi_social_channels -------------- ' )	
		result = {}
		#logger.debug(self.creaListaFields())
		for chan in ['fblivesocencchan','ioutubelivesocencchan']:
			logger.debug(chan)
			__field_chan = self.prendiField( chan )
			__list = []
			__list = __field_chan.findall(namespaces['vdf'] + 'list' )
			if len(__list) == 0:
				continue
			else: 
				logger.debug('ci sono valori nella lista')
				logger.debug('prendo il payload')
				__pay = __list[0].findall( "vdf:payload")
				if len(__pay) == 0:
					__pay = __list[0].findall(namespaces['vdf'] + "payload")
				logger.debug('__pay : ' + str(__pay))
				if len(__pay) == 0:
					continue
				__social_channels = __pay[0].findall(namespaces['vdf'] + "field")
				if len(__social_channels) == 0 or not (chan in __social_channels[0].attrib['name']):
					logger.debug(__social_channels)
					continue
				__social_field = __social_channels[0].findall(namespaces['vdf']  + "field")
				for __soc in __social_field:
					if 'livesocialid' in __soc.attrib['name']:
						# devo prenderne il value
						__fieldValue = __soc.find( namespaces['vdf'] +'value' )
						if not __fieldValue is None:
							result[ __fieldValue.text ] =  __social_channels[0]
						else:
							__fieldValue = __soc.find( 'vdf:value' )
							if not __fieldValue is None:
								result[ __fieldValue.text ] =  __social_channels[0]
				
		logger.debug( result)
		logger.debug ( '------------------------ end prendi_social_channels -------------- ' )	
		return result



	def Old_sistemaSocials_Old( self ) :

		#logger.debug(result)
		# devo girare sui channel e fare le cose opportune
		logger.debug ( '------------------------ INIT  sistemaSocials -------------- ' )

		logger.debug( self.assetdata)

		arr = []
		if 'socialChannels' in self.assetdata:
			arr = self.assetdata['socialChannels']
			logger.debug(arr)
		else:
			logger.debug('AGGIUNTO il 12.10.2023 ...... DEBUGGARE ! ')
			return	
		
		tmpFBresult = None
		tmpYTresult = None

		logger.debug ( sorted(arr,key = itemgetter('platformType'), reverse=True))

		# metto i valori di default per web e hbbtv cosi' nel caso non vengano riscritti 
		# ho i valori nulli
		
		for chan in self.assetdata['socialChannels']:
			if 'facebook' in chan['platformType'] or 'FB' in chan['platformType'] :
				# oppure se sono Social
				# devo creare la struttura Social opportuna
				logger.debug( 'creo FB')
				# se platformType == facebook devo creare una entry nella lista
				# fblivesocencchan con il payload giusto
				tmpFBresult = self.creaSocialXml(tmpFBresult, chan, 'fblivesocencchan' )
				

			elif 'youtube' in chan['platformType'] or 'YOUTUBE' in chan['platformType'] :
				# se platformType == youtube  devo creare una entry nella lista
				# ioutubelivesocencchan con il payload giusto
				logger.debug( 'creo youtube')
		
				# ocio che va incapsulato nel caso sia una lista con piu elementi
				tmpYTresult = self.creaSocialXml(tmpYTresult, chan, 'ioutubelivesocencchan' )

				
		logger.debug ( '------------------------ MIDDLE  sistemaSocials -------------- ' )

		logger.debug(tmpFBresult)
		self.assetdata['fblivesocencchan'] = tmpFBresult
		self.assetdata['ioutubelivesocencchan'] = tmpYTresult

		if 'fblivesocencchan' in self.assetdata and not(self.assetdata['fblivesocencchan'] is None):
			# in self.assetdata['fblivesocencchan'] ho un element da inserire
			self.mettiNullaSocialList( 'fblivesocencchan')
			self.cambiaSocialList( 'fblivesocencchan', self.assetdata['fblivesocencchan']  )
		else:
			# devo aggiungere la lista nulla al nodo opportuno
			logger.debug('------------------------------------- passo da mettinulla')
			self.mettiNullaSocialList( 'fblivesocencchan')

		if 'ioutubelivesocencchan' in self.assetdata and not(self.assetdata['ioutubelivesocencchan'] is None):
			# in self.assetdata['fblivesocencchan'] ho un element da inserire
			self.mettiNullaSocialList(  'ioutubelivesocencchan')
			self.cambiaSocialList( 'ioutubelivesocencchan', self.assetdata['ioutubelivesocencchan']  )
		else:
			# devo aggiungere la lista nulla al nodo opportuno
			logger.debug('------------------------------------- passo da mettinulla')
			self.mettiNullaSocialList(  'ioutubelivesocencchan')

		if 'webextraStream' in  self.assetdata and not(self.assetdata['webextraStream'] is None):
			# in self.assetdata['fblivesocencchan'] ho un element da inserire
			nodo = self.creaExtraStreamXML( self.assetdata )
			self.mettiNullaSocialList(  'webextraStream')
			self.cambiaSocialList( 'webextraStream', nodo  )
		else:
			# devo aggiungere la lista nulla al nodo opportuno
			logger.debug('------------------------------------- passo da mettinulla')
			self.mettiNullaSocialList(  'webextraStream')
		
		
	def cambiaSocialList( self, fieldName, val ):

		list =  self.root.findall(namespaces['atom'] + "content")
		for lis in list:
			payload =  lis.findall(namespaces['vdf'] + "payload")
			for pay in payload:
				fields = pay.findall(namespaces['vdf'] + "field")
				#logger.debug(fields)

				for idx , fiel in enumerate(fields):
					#logger.debug(idx, fiel)
					#logger.debug(fiel.attrib['name'])
					if fieldName in fiel.attrib['name'] and len( fieldName) == len(fiel.attrib['name']):
						fiel.append(val)
						return entry

		return entry
		
	def mettiNullaSocialList( self, fieldName ):

		list =  self.root.findall(namespaces['atom'] + "content")
		for lis in list:
			payload =  lis.findall(namespaces['vdf'] + "payload")
			for pay in payload:
				fields = pay.findall(namespaces['vdf'] + "field")
				#logger.debug(fields)

				for idx , fiel in enumerate(fields):
					#logger.debug(idx, fiel)
					#logger.debug(fiel.attrib['name'])
					if fieldName in fiel.attrib['name'] and len( fieldName) == len(fiel.attrib['name']):
						# devo rimuovere quello vecchio e farne uno nuovo
						pay.remove( fiel )
						nuovo = ET.Element(namespaces['vdf'] + "field")
						nuovo.set('name' , fieldName)
						
						pay.append(nuovo)
						return


	def creaExtraStreamXML( self ):
		
		logger.debug ( '------------------------ INIT creaExtraStreamXML -------------- ' )

		# crea  l'html di un social channel da attaccare come lista sotto l'elemento opportuno
		root = ET.Element("list")
		
		# ocio che va incapsulato nel caso sia una lista con piu elementi
		# e non basta fare il testo ma bisogna fare gli annidamenti giusti
		node =  ET.Element(namespaces['vdf']  + 'list')

		urls = [ 'hlsURL','hdsURL']
		
		for urlEntry in urls:

			# adesso  devo creare payload
			payload = ET.Element(namespaces['vdf']  + 'payload')
			# e adesso una sequenza di createFields con i valori che ci sono in chan
			# tutti da appendere a "name"
			fiel = creaField( 'webextraStream', jsonToClean[urlEntry] )
			logger.debug( 'passo da : ' + urlEntry + ' con val : ' + jsonToClean[urlEntry] )
			payload.append( fiel )

			# ocio ad encoder che manca
			node.append(payload )
		
		# DEBUG
		#ET.dump( node )
		#exit(0)
		
		logger.debug ( '------------------------ END creaExtraStreamXML -------------- ' )
		return node
		
	def creaField(self,  name, value ):

		fiel = ET.Element(namespaces['vdf'] + "field")
		fiel.set("name", name )
		fiel.append(ET.Element(namespaces['vdf'] + "value"))
		fiel.find(namespaces['vdf'] + "value").text = value
		return fiel

	def copiaSocialXml( self, node, veteran ):
		
		logger.debug ( '------------------------ INIT copiaSocialXml -------------- ' )
		result = ''

		# ocio che va incapsulato nel caso sia una lista con piu elementi
		# e non basta fare il testo ma bisogna fare gli annidamenti giusti
		if node is None :
			# sono alla prima passata e devo mettere 
			# e ci va un "<vdf:list>" all inizio 
			node =  ET.Element(namespaces['vdf']  + 'list')

		# adesso  devo creare payload
		payload = ET.Element(namespaces['vdf']  + 'payload')
		payload.append( veteran )

		# ocio ad encoder che manca
		node.append(payload )
		
		# DEBUG
		#ET.dump( node )
		#logger.debug(str(ET.tostring(node, encoding='utf8', method='xml').decode('utf8')))
		#result = str(ET.tostring(node, encoding='utf8', method='xml').decode('utf8'))
		
		# e ci va un "</vdf:list>" alla fine
		logger.debug ( '------------------------ END copiaSocialXml -------------- ' )
		# passo il nodo perche poi lo sistemo sull xml con ET
		return node


	def creaSocialXml( self, node, channel, kind ):
		
		logger.debug ( '------------------------ INIT creaSocialXml -------------- ' )
		result = ''

		# crea  l'html di un social channel da attaccare come lista sotto l'elemento opportuno
		root = ET.Element("list")
		

		soc = self.aggiungiSocial( channel )
		logger.debug( soc )

		# ocio che va incapsulato nel caso sia una lista con piu elementi
		# e non basta fare il testo ma bisogna fare gli annidamenti giusti
		if node is None :
			# sono alla prima passata e devo mettere 
			# e ci va un "<vdf:list>" all inizio 
			node =  ET.Element(namespaces['vdf']  + 'list')

		# adesso  devo creare payload
		payload = ET.Element(namespaces['vdf']  + 'payload')
		name = ET.Element(namespaces['vdf']  + "field")
		name.set("name", kind )
		payload.append( name )

		# e adesso una sequenza di createFields con i valori che ci sono in chan
		# tutti da appendere a "name"
		for key,val in soc.items():
			fiel = self.creaField( key, val )
			name.append( fiel )

		# ocio ad encoder che manca
		node.append(payload )
		
		# DEBUG
		#ET.dump( node )
		#logger.debug(str(ET.tostring(node, encoding='utf8', method='xml').decode('utf8')))
		#result = str(ET.tostring(node, encoding='utf8', method='xml').decode('utf8'))
		
		# e ci va un "</vdf:list>" alla fine
		logger.debug ( '------------------------ END creaSocialXml -------------- ' )
		# passo il nodo perche poi lo sistemo sull xml con ET
		return node
		

	def aggiungiSocial( self, channel ):
		logger.debug(' ---------- INIT aggiungiSocial -------------- ')
		result = channel
		
		soc = {}

		if 'platformTitle' in channel:
			soc['videoTitle'] =channel['platformTitle']
		if 'platformDescription' in channel:
			soc['videoDesc'] = channel['platformDescription']

		if 'platformNotificationDate' in result:
			result['platformNotificationDate'] = str(result['platformNotificationDate'])
			if 'Z' in result['platformNotificationDate']:
				logger.debug( 'arrivata platformNotificationDate dal Programme' )
				# mi e' arrivata la data gia nel formato giusto
				data = result['platformNotificationDate']
				logger.debug( data )
			else :
				logger.debug( 'trovato platformNotificationDate' )
				timestamp = int(result['platformNotificationDate'])/1000.0
				logger.debug( timestamp )
				value = datetime.utcfromtimestamp(timestamp)
				data = value.strftime("%Y-%m-%dT%H:%M:%SZ")
				logger.debug( data )
			result['platformNotificationDate'] = data
			soc['notificaTime'] =result['platformNotificationDate'] # da trasformare

		if 'platformChannel' in channel:
			soc['livestreamingaccount'] =channel['platformChannel']
		if 'platformIsGeoBlocked' in channel:
			soc['isGeoBlocked'] =str(channel['platformIsGeoBlocked'])
		if 'platformId' in channel:
			soc['livesocialid'] =str(channel['platformId'])

		logger.debug(' ---------- END aggiungiSocial -------------- ')
		return soc	


	def PrendiExtraStream( entry ):

		result = []
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
					if 'extraStream' == fiel.attrib['name']:
						#logger.debug('passo di qui')
						# qui ho preso il field fb-livestreaming-account
						# e adesso devo prendere tutti gli account che ho messo
						_list = fiel.findall(namespaces['vdf'] + "list")
						if len(_list) > 0:
							_list = _list[0]
						else:
							return False
						stre_payloads =  _list.findall(namespaces['vdf'] + "payload")
						#logger.debug('stre_payloads ')
						#logger.debug(stre_payloads)
						for stre in stre_payloads:
							#logger.debug('giro _payloads')
							#logger.debug(stre)
							stre_field = stre.find(namespaces['vdf'] + "field")
							#logger.debug(stre_field.attrib['name'])
							if 'extraStream' in stre_field.attrib['name']:
								if not (stre_field.find(namespaces['vdf'] + "value") is None) :
									#logger.debug(stre_field.find(namespaces['vdf'] + "value").text)
									result.append( stre_field.find(namespaces['vdf'] + "value").text )
									#result.append(acc_field.find(namespaces['vdf'] + "value").text)

		return result








if __name__ == "__main__":

	jsonToCreate = {'summary':'summary TEXT debug','video_normalized': True, 'video_clips': [{'markOut': 1668089790761, 'markIn': 1668089747707}], 'video__rev': '9-66a717a09e4899ccfeb79f75494fba14', 'video_channel': 'la1', 'video_cms_asset_urn': '1253414', 'video_awsKeyframe_url': 'https://rsi-mam-poster-frames-master.s3.eu-west-1.amazonaws.com/la1_1678226414000.jpg', 'video_awsKeyframe_status': 'SUCCEEDED', 'video_section': 5, 'video_source': 'mam-gui', 'video_title': 'Verifica logo', 'video_composedEvent': False, 'video_assetType': 'manualCut', 'video_urn': 'rsi:mam:video:66f1161f0969c959931d8b19abcf90a9', 'video_QoS': 'RSI_VIDEO_HD720', 'video_editorialKeyframe': 1668089790761, 'video_rights_expireDate': '', 'video_rights_geoblocked': False, 'video_rights_activationDate': '2022-11-10T14:58:41.052Z', 'video_logo': 'RSI_LOGO_NEWS', 'video__id': '66f1161f0969c959931d8b19abcf90a9', 'video_lastupdate': '2022-11-10T15:00:19.659Z', 'video_geoblocked': False, 'video_transcoderMetadata_urn': 'urn:rsi:aws:la1-fcc5c1af-7a7c-4026-bd1e-db5d950de9db', 'video_transcoderMetadata_transcodedAssets': [{'duration': 43123, 'width': 1280, 'bitrate': 3400000, 'backup_url': 'https://mam-stag.rsi.ch/download-asset/cnNpLW1hbS10cmFuc2NvZGVkLWFzc2V0cy1zdGFnaW5nL3JzaS13dy8yMDIyLzExLzEwLzY2ZjExNjFmMDk2OWM5NTk5MzFkOGIxOWFiY2Y5MGE5XzIwMjIxMTEwXzE0NTk0M183MjAubXA0', 'uri': 's3://rsiori-int/rsi-ww/2022/11/10/66f1161f0969c959931d8b19abcf90a9_20221110_145943_720.mp4', 'height': 720}, {'duration': 43123, 'width': 640, 'bitrate': 1200000, 'backup_url': 'https://mam-stag.rsi.ch/download-asset/cnNpLW1hbS10cmFuc2NvZGVkLWFzc2V0cy1zdGFnaW5nL3JzaS13dy8yMDIyLzExLzEwLzY2ZjExNjFmMDk2OWM5NTk5MzFkOGIxOWFiY2Y5MGE5XzIwMjIxMTEwXzE0NTk0M18zNjAubXA0', 'uri': 's3://rsiori-int/rsi-ww/2022/11/10/66f1161f0969c959931d8b19abcf90a9_20221110_145943_360.mp4', 'height': 360}, {'duration': 43123, 'width': 480, 'bitrate': 300000, 'backup_url': 'https://mam-stag.rsi.ch/download-asset/cnNpLW1hbS10cmFuc2NvZGVkLWFzc2V0cy1zdGFnaW5nL3JzaS13dy8yMDIyLzExLzEwLzY2ZjExNjFmMDk2OWM5NTk5MzFkOGIxOWFiY2Y5MGE5XzIwMjIxMTEwXzE0NTk0M18yNzIubXA0', 'uri': 's3://rsiori-int/rsi-ww/2022/11/10/66f1161f0969c959931d8b19abcf90a9_20221110_145943_272.mp4', 'height': 272}], 'video_transcoderMetadata_status': 'COMPLETED', 'video_transcoderMetadata_keyFrames': [{'url': 'https://rsi-mam-poster-frames-master.s3.eu-west-1.amazonaws.com/la1_1678226414000.jpg', 'timestamp': 1668089790761}], 'video_day': '2022-11-10', 'video_user_name': 'Trapletti, Roberto (RSI)', 'video_user_id': '7e7c41ca-9c58-4fea-99e4-0916f257d9f0', 'video_user_email': 'Roberto.Trapletti@rsi.ch', 'video_contentType': 'mamTranscodableVideo', 'video_status': 'COMPLETED', 'url': 'https://rsi-mam-poster-frames-master.s3.eu-west-1.amazonaws.com/la1_1678226414000.jpg', 'status': 'SUCCEEDED', 'contentType': 'keyframe', 'section': '5235', 'message': {'video': {'normalized': True, 'clips': [{'markOut': 1668089790761, 'markIn': 1668089747707}], '_rev': '9-66a717a09e4899ccfeb79f75494fba14', 'channel': 'la1', 'cms': {'asset': {'urn': '1253414'}}, 'awsKeyframe': {'url': 'https://rsi-mam-poster-frames-master.s3.eu-west-1.amazonaws.com/la1_1678226414000.jpg', 'status': 'SUCCEEDED'}, 'section': 5, 'source': 'mam-gui', 'title': 'Verifica logo', 'composedEvent': False, 'assetType': 'manualCut', 'urn': 'rsi:mam:video:66f1161f0969c959931d8b19abcf90a9', 'QoS': 'RSI_VIDEO_HD720', 'editorialKeyframe': 1668089790761, 'rights': {'expireDate': '', 'geoblocked': False, 'activationDate': '2022-11-10T14:58:41.052Z'}, 'logo': 'RSI_LOGO_NEWS', 'urn': '66f1161f0969c959931d8b19abcf90a9', 'lastupdate': '2022-11-10T15:00:19.659Z', 'geoblocked': False, 'transcoderMetadata': {'urn': 'urn:rsi:aws:la1-fcc5c1af-7a7c-4026-bd1e-db5d950de9db', 'transcodedAssets': [{'duration': 43123, 'width': 1280, 'bitrate': 3400000, 'backup_url': 'https://mam-stag.rsi.ch/download-asset/cnNpLW1hbS10cmFuc2NvZGVkLWFzc2V0cy1zdGFnaW5nL3JzaS13dy8yMDIyLzExLzEwLzY2ZjExNjFmMDk2OWM5NTk5MzFkOGIxOWFiY2Y5MGE5XzIwMjIxMTEwXzE0NTk0M183MjAubXA0', 'uri': 's3://rsiori-int/rsi-ww/2022/11/10/66f1161f0969c959931d8b19abcf90a9_20221110_145943_720.mp4', 'height': 720}, {'duration': 43123, 'width': 640, 'bitrate': 1200000, 'backup_url': 'https://mam-stag.rsi.ch/download-asset/cnNpLW1hbS10cmFuc2NvZGVkLWFzc2V0cy1zdGFnaW5nL3JzaS13dy8yMDIyLzExLzEwLzY2ZjExNjFmMDk2OWM5NTk5MzFkOGIxOWFiY2Y5MGE5XzIwMjIxMTEwXzE0NTk0M18zNjAubXA0', 'uri': 's3://rsiori-int/rsi-ww/2022/11/10/66f1161f0969c959931d8b19abcf90a9_20221110_145943_360.mp4', 'height': 360}, {'duration': 43123, 'width': 480, 'bitrate': 300000, 'backup_url': 'https://mam-stag.rsi.ch/download-asset/cnNpLW1hbS10cmFuc2NvZGVkLWFzc2V0cy1zdGFnaW5nL3JzaS13dy8yMDIyLzExLzEwLzY2ZjExNjFmMDk2OWM5NTk5MzFkOGIxOWFiY2Y5MGE5XzIwMjIxMTEwXzE0NTk0M18yNzIubXA0', 'uri': 's3://rsiori-int/rsi-ww/2022/11/10/66f1161f0969c959931d8b19abcf90a9_20221110_145943_272.mp4', 'height': 272}], 'status': 'COMPLETED', 'keyFrames': [{'url': 'https://rsi-mam-poster-frames-master.s3.eu-west-1.amazonaws.com/la1_1678226414000.jpg', 'timestamp': 1668089790761}]}, 'day': '2022-11-10', 'user': {'name': 'Trapletti, Roberto (RSI)', 'id': '7e7c41ca-9c58-4fea-99e4-0916f257d9f0', 'email': 'Roberto.Trapletti@rsi.ch'}, 'contentType': 'mamTranscodableVideo', 'status': 'COMPLETED'}, 'url': 'https://rsi-mam-poster-frames-master.s3.eu-west-1.amazonaws.com/la1_1678226414000.jpg', 'status': 'SUCCEEDED', 'contentType': 'keyframe'}, 'title': '66f1161f0969c959931d8b19abcf90a9_la1_1678226414000.jpg'}

	ct = MasterType(None, None,jsonToCreate)
	ct.createDocument()
	ct.dumpDoc()
	exit(0)

	# 'CUE_USER' : 'TSMM', 'CUE_PWD':'8AKjwWXiWAFTxb2UM3pZ'

	os.environ['CUE_USER'] = 'rsi_admin'
	os.environ['CUE_PWD'] = 'admin'

	cueServer = 'http://10.101.8.38:8080'
	cueServer = 'http://18.158.61.219:8080'
	cueServer = 'https://cue.cue-test.rsi.ch'
	cueAdmin = 'https://admin.cue-test.rsi.ch'


	os.environ['CUE_MODEL'] = cueServer + '/webservice/publication/rsi/escenic/model/'
	os.environ['CUE_CONTENTTYPE'] = cueServer + '/webservice/escenic/publication/rsi/model/content-type/'
	os.environ['CUE_SECTION_MODEL'] = cueServer + '/webservice/escenic/publication/rsi/model/content-type/com.escenic.section'
	os.environ['CUE_SECTION'] = cueServer + '/webservice/escenic/section/'
	os.environ['CUE_CONTENT'] = cueServer + '/webservice/escenic/content/'
	os.environ['CUE_SERVER'] = cueServer
	os.environ['CUE_BINARY' ] =  cueServer + '/webservice/escenic/binary'
	os.environ['CUE_SECTION_PARAMETERS'] = cueAdmin + '/escenic-admin/section-parameters-declared/rsi'

	os.environ['IMG_CREATE_URL'] = cueServer + '/webservice/escenic/section/__CREATE_SECTION__/content-items'
	os.environ['RESOURCE_DIR'] = '/home/perucccl/PRODUCTION/article-structure-mananager/Resources/'



	putSectionParameters('/', '/home/perucccl/PRODUCTION/article-structure-mananager/LOGS/FILES/sectionparams_06.09.2022_16.31.06.810824.xml' )
	exit(0)

	#subsectionXml = getSubSections( 'https://cue.cue-test.rsi.ch/webservice/escenic/section/1/subsections' )
	#logger.debug(type(subsectionXml))
	#xmlPiccoloParser = xmlService.xmlPiccoloParser( subsectionXml )
	#logger.debug(xmlPiccoloParser.prendiListaEntry())
	#exit(0)

	#listaDel = [ 3 ]
	listaDel = [ 27,3,9,11,24,25,26 ]
	listaDel = [2177]
	for lis in listaDel:
		deleteSection( str(lis) )

	# se stai cancellando le sezioni di CUE ricordati
	# di toglierle dal SQL 
	# MA di aggiungere 4-1 e 5-2
	exit(0)

	#createSectionFromFile("/home/perucccl//PRODUCTION/article-structure-mananager/LOGS/FILES/section_19.05.2022_23.28.59.629005.xml")	
	#exit(0)
	#logger.debug(createSectionFromFile( '/home/perucccl/PRODUCTION/article-structure-mananager/LOGS/FILES/section_20.05.2022_17.26.12.880872.xml'))
	logger.debug(putSectionId( '28', './section28.xml' ))
	exit(0)

	logger.debug(getSection( '28' ))
	exit(0)

	deleteSection( '39' )
	exit(0)

	putSection('4097', './4097.xml')
	exit(0)
	putSectionId('4097', './4097.xml')
	exit(0)
	logger.debug(result)
	exit(0)
	getId( '14915243' )

