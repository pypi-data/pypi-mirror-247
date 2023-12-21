import re
import os
from datetime import datetime, timedelta
import logging
import json
import urllib


import time
from datetime import datetime, timezone
from dateutil import tz
from dateutil.parser import parse

# per prendere le img dall s3 con boto
import boto3
#ACCESS_KEY = 'AKIA4HLRXFHOYXC7KEXV'
#SECRET_KEY = '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'
#BUCKET_NAME = 'rsiori-prd'

import rsi_python_lib.pyCueServices as cueServices
import rsi_python_lib.xmlService as xmlService
import rsi_python_lib.pyCueContenType as CCType
import rsi_python_lib.pyConfig as pyConfig
import rsi_python_lib.pySettaVars as pySettaVars

logger = logging.getLogger()

def SettaEnvironment( debug ):

        if (debug):
                logger.debug( 'PRIMA DI SETTARE ENVIRONMENT')
        if (debug):
                logger.debug( 'ENV : ')
        if (debug):
                logger.debug( os.environ)

        if (debug):
                logger.debug( '---------------------------------')

        logger.debug( 'verifico il setting della variabile _rsi_env_ ')
        if '_rsi_env_' in os.environ:
                if 'PRODUCTION' in os.environ['_rsi_env_']:
                        logger.debug( 'variabile _rsi_env_ ha valore \'PRODUCTION\'')
                        logger.debug( 'setto ENV di PROD')
                        config = pyConfig.config('PROD')
                        pySettaVars.sectionMapping = pySettaVars.sectionMapping_PROD
                else:
                        logger.debug( 'variabile _rsi_env_ ha valore : ' + os.environ['_rsi_env_'])
                        logger.debug( 'diverso da \'PRODUCTION\'')
                        logger.debug( 'setto ENV di STAG')
                        config = pyConfig.config('STAG')
                        pySettaVars.sectionMapping = pySettaVars.sectionMapping_STAG

        else:
                logger.debug( 'variabile _rsi_env_ non trovata: setto ENV di STAG')
                config = pyConfig.config('STAG')
                pySettaVars.sectionMapping = pySettaVars.sectionMapping_STAG

        if (debug):
                logger.debug( 'DOPO AVER SETTATO ENVIRONMENT')
        if (debug):
                logger.debug( 'ENV : ')
        if (True):
                logger.debug( os.environ)


def ritornDateSitemapDecimal( date ):

	date = parse( date )
	result =  int(date.timestamp() * 1000.0)
	#logger.debug( int( result ))
	return result

def sistemaDateSitemapDecimal( date ):

	dt_object = datetime.utcfromtimestamp(date/1000)
	from_zone = tz.gettz('UTC')
	to_zone  = tz.gettz('Europe/Madrid')
	start_date = dt_object.replace(tzinfo = from_zone)
	local = start_date.astimezone(to_zone)
	return str(local).replace(' ','T')

def sistemaDateSitemapString( date ):

	# la data ora emntra come string 2023-06-08T16:44:00Z
	date_format = '%Y-%m-%dT%H:%M:%SZ'
	dt_object = datetime.strptime(date, date_format)
	from_zone = tz.gettz('UTC')
	to_zone  = tz.gettz('Europe/Madrid')
	start_date = dt_object.replace(tzinfo = from_zone)
	local = start_date.astimezone(to_zone)
	return str(local).replace(' ','T')

def sistemaDateSitemap( date ):
	try:
		result = sistemaDateSitemapDecimal( date )
	except:
		if 'Z' in date:
			result = sistemaDateSitemapString( date )
		else:
			# vuol dire che sono gia entrato con data con timezone
			# generalmente sono arrivate dalla update 
			result = date

	return result






def pulisciXml( message ):

	# per togliere dalle balle le inutili intestazioni ( gia presenti nelle labels )
	# e avere gli id puliti
	# e cambiare i loghi
	result = {}

	daTogliere = {
		'rsi:escenic:mamProgramme:' : '',
		'rsi:escenic:programme:' : '',
		'rsi:escenic:mamProgrammeVideo:' : '',
		'rsi:escenic:programmeVideo:' : '',
		'rsi:escenic:mamTranscodableVideo:' : '',
		'rsi:escenic:transcodableVideo:' : '',
		'rsi:escenic:mamTranscodableAudio:' : '',
		'rsi:escenic:transcodableAudio:' : '',
		'rsi:escenic:livestreaming:' : '',
		'rsi:escenic:mamSegmentedProgrammeVideo:' : '',
		'rsi:escenic:segmentedProgrammeVideo:' : '',
		'rsi:cue:video:':'',
		'rsi:cue:videosegment:':'',
		'rsi:cue:audiosegment:':'',
		'rsi:cue:livestreaming:' : '',
		'LOGO ROSSO' : 'logoRosso',
		'LOGO GIALLO' : 'logoGiallo',
		'RSI La1 - TG 20:00 ' : '',
		'RSI La1 - TG 12:30 ' : '',
		'RSI La1 - QUOTIDIANO ESTATE ' : '',
		'RSI La1 - QUOTIDIANO ' : '',
		'&' : '&amp;'
	}
	
	daTogliereOk = {
		'rsi:mp:louise:' : '',
		'rsi:mp:playlist:' : '',
		'rsi:mam:video:' : '',
		'rsi:mam:audio:' : '',
		'rsi:escenic:mamProgramme:' : '',
		'rsi:escenic:programme:' : '',
		'rsi:escenic:mamProgrammeVideo:' : '',
		'rsi:escenic:programmeVideo:' : '',
		'rsi:escenic:mamTranscodableVideo:' : '',
		'rsi:escenic:transcodableVideo:' : '',
		'rsi:escenic:mamTranscodableAudio:' : '',
		'rsi:escenic:transcodableAudio:' : '',
		'rsi:escenic:mamSegmentedProgrammeVideo:' : '',
		'rsi:escenic:segmentedProgrammeVideo:' : '',
		'LOGO ROSSO' : 'logoRosso',
		'LOGO GIALLO' : 'logoGiallo',
		'RSI La1 - TG 20:00 ' : '',
		'RSI La1 - TG 12:30 ' : '',
		'RSI La1 - QUOTIDIANO ESTATE ' : '',
		'RSI La1 - QUOTIDIANO ' : '',
		'&' : '&amp;'
	}
	
	try:
		messageStr = json.dumps( message )
		# use these three lines to do the replacement
		rep = dict((re.escape(k), v) for k, v in daTogliere.items()) 
		pattern = re.compile("|".join(rep.keys()))
		text = pattern.sub(lambda m: rep[re.escape(m.group(0))], messageStr)
		xmlStr = text

		logger.debug ( xmlStr )
		logger.debug( xmlStr )
		result = json.loads( xmlStr )

	except Exception as e:
		logger.warning( 'Problemi in pulisciXml : ' + str(e) )
		pass

	return result

def sistemaTitolo( titolo ):

	caratteriSpeciali =  {'&':'&#38;','<':'&lt;','>':'&gt;'}
	# use these three lines to do the replacement
	rep = dict((re.escape(k), v) for k, v in caratteriSpeciali.items()) 
	pattern = re.compile("|".join(rep.keys()))
	result = pattern.sub(lambda m: rep[re.escape(m.group(0))], titolo)
	logger.debug(result)
	return  result


def togliAccenti( accentata ):
	result = ''
	# qui dichiaro cosa devo cambiare
	repl = str.maketrans(
		"àáâãäèéêëìíîïòóôöùúûü",
		"aaaaaeeeeiiiioooouuuu"
	)

	try :
		result = accentata.translate(repl)
	except Exception as e:
		logger.warning( 'Problemi in togliAccenti : ' + str(e) )
		pass

	return result

def rimpiazzaIlResto( brand ):

	brand = brand.replace(" ", "-")
	brand = brand.replace("&amp;", "_")
	brand = brand.replace("-_-", "-")
	brand = brand.replace("'", "")
	brand = brand.replace("?", "")
	brand = brand.replace("!", "")
	brand = brand.replace("\\", "")
	brand = brand.replace("/", "")
	brand = brand.replace(",", "")
	brand = brand.replace("'", "")
	brand = brand.replace("’", "")
	brand = brand.replace("(", "-")
	brand = brand.replace(")", "-")
	brand = brand.replace("---", "-")
	brand = brand.replace("--", "-")
	brand = brand.replace("...", "")
	brand = brand.replace("..", "")
	brand = brand.replace("…", "")
	brand = brand.replace(".", "-")
	brand = brand.replace(":", "")
	brand = brand.replace("°", "")
	brand = brand.replace("jamie-oliver-menu-in-30-minuti", "jamie-oliver-menu-in-15-minuti")
	brand = brand.replace("rock-legends", "documentari-intrattenimento")
	brand = brand.replace("troppo-giovane-per-morire", "documentari-intrattenimento")
	brand = brand.replace("pop-profiles", "documentari-intrattenimento")
	brand = brand.replace("documentari-musicali", "documentari-intrattenimento")
	brand = brand.replace("hank-zipzer-fuori-dalle-righe-anno-3-", "hank-zipzer-fuori-dalle-righe")
	brand = brand.replace("alta-fedelta-una-vita-da-cani", "alta-fedelta")
	brand = brand.replace("cash-professioni", "cash")
	brand = brand.replace("colazione-con-peo", "peo")
	brand = brand.replace("quartier-des-banques-l-affare-grangier","quartier-des-banques")
	brand = brand.replace("locarno-film-festival-72","locarno-festival")
	brand = brand.replace("locarno-film-festival-73","locarno-festival")
	brand = brand.replace("locarno-film-festival-74","locarno-festival")
	brand = brand.replace("locarno-film-festival-75","locarno-festival")
	brand = brand.replace("serata-tematica","serate-tematiche")
	brand = brand.replace("filo-diretto-prima-parte","filo-diretto")
	brand = brand.replace("filo-diretto-seconda-parte","filo-diretto")
	brand = brand.replace("filo-diretto-terza-parte","filo-diretto")
	brand = brand.replace("svizzera-e-dintorni-in-cammino-sulla-via-idra","svizzera-e-dintorni")
	brand = brand.replace("avvicinamento-alle-elezioni-comunali-2020", "elezioni-cantonali-ticinesi-2019")
	brand = brand.replace("avvicinamento-alle-elezioni-comunali-2021", "elezioni-cantonali-ticinesi-2019")
	brand = brand.replace("vacanze-a-km-0-il-viaggio", "vacanze-a-km-0")
	brand = brand.replace("speciale-votazioni", "democrazia-diretta")
	brand = brand.replace("avvicinamento-alle-elezioni-comunali-2021", "elezioni-cantonali-ticinesi-2019")
	brand = brand.replace("elezioni-comunali-2021", "elezioni-cantonali-ticinesi-2019")
	brand = brand.replace("moviola-340-estate", "moviola-340")
	brand = brand.replace("falo-estate", "falo")
	brand = brand.replace("la-domenica-sportiva-estate", "la-domenica-sportiva")
	brand = brand.replace("giornata-elezioni-federali", "elezioni-cantonali-ticinesi")

	# replace dei cartoni
	for unTmp in pySettaVars.listaCartoniUniqueNames:
		brand = brand.replace(unTmp, "cartoni-e-serie-per-bambini" )
	if "cartoni-e-serie-per-bambini" in brand:
		channel = 'la1'

	if "serata-speciale-informazione" in brand:
		channel = 'la2'

	# replace degli spazi con "-" es: Criminal minds --> brand=criminal-minds
	brand = brand.replace(' ', '-')
	# replace dei caratteri speciali con "-". es Grey's anatomy --> brand = grey-s-anatomy
	brand = brand.replace('\'','-').replace('\"', '-')

	return brand

	
def sistemaTitolo( titolo ):

	# use these three lines to do the replacement
	rep = dict((re.escape(k), v) for k, v in pySettaVars.caratteriSpeciali.items()) 
	pattern = re.compile("|".join(rep.keys()))
	result = pattern.sub(lambda m: rep[re.escape(m.group(0))], titolo)
	logger.debug(result)
	return  result

def creaNomeFileJpg( contentType ):

	dateTimeObj = datetime.now()
	timestampStr = dateTimeObj.strftime("%d.%m.%Y_%H.%M.%S.%f")
	result = os.environ['CUE_CREATE_FILES'] +  contentType + '_' + timestampStr + '.jpg'
	return result


def creaNomeFileList( contentType ):

	dateTimeObj = datetime.now()
	timestampStr = dateTimeObj.strftime("%d.%m.%Y_%H.%M.%S.%f")
	result = os.environ['CUE_CREATE_FILES'] +  contentType + '_' + timestampStr + '.list'
	return result
	



def creaNomeFile( contentType ):

	dateTimeObj = datetime.now()
	timestampStr = dateTimeObj.strftime("%d.%m.%Y_%H.%M.%S.%f")
	result = os.environ['CUE_CREATE_FILES'] +  contentType + '_' + timestampStr + '.xml'
	return result
	

def prendiS3Img( fileS3Url ):
	result = None
	logger.debug('------------------------ INIT prendiS3Img -------------- ')

	try:
		logger.debug( 'link : ' + fileS3Url  )
		logger.info( 'link  prendiS3Img: ' + fileS3Url  )
		link = fileS3Url
		
		request = urllib.request.Request(url=link,  method='GET')
		#request.add_unredirected_header('Authorization', 'Bearer %s' % 'n2qefrD42juHkzAqrVaStvBUgsZHjN')
		#resultResponse = urllib.request.urlopen(request)
		with urllib.request.urlopen(request) as resultResponse:
			logger.debug ( resultResponse.status )
			#result = resultResponse.data
			logger.debug ( resultResponse.headers )
			#logger.debug ( resultResponse.headers )
			#logger.debug ( resultResponse.headers.split('rsi.ch/webservice/escenic/content/' )[-1] )
			logger.debug ( resultResponse.reason )
			result = resultResponse.read()

	except Exception as e:
		logger.debug ( 'PROBLEMI in prendiS3Img : ' + str(e) )
		logger.debug ( 'PROBLEMI in prendiS3Img : ' + str(e) )
		return [ False, { 'error' : str(e) } ]
	logger.debug('------------------------ END prendiS3Img -------------- ')
	return result

def prendiS3ImgBoto3( fileS3Url ):
	result = ''
	logger.debug('------------------------ INIT prendiS3ImgBoto3 CLAD -------------- ')

	try:
		objName = fileS3Url.split('amazonaws.com/')[-1]
		logger.debug( 'objName = ' + str(objName)  )
	
		filename = creaNomeFileJpg( 'immagineS3Boto' )
		logger.debug('boto3 filename = ' + filename)
		s3 = boto3.client('s3', aws_access_key_id=os.environ['AWS_S3_ACCESSKEY'] , aws_secret_access_key=os.environ['AWS_S3_SECRETKEY'] )
		s3.download_file(os.environ['AWS_S3_BUCKET'], objName, filename)

	except Exception as e:
		logger.debug ( 'PROBLEMI in prendiS3ImgBoto3 : ' + str(e) )
		logger.debug ( 'PROBLEMI in prendiS3ImgBoto3 : ' + str(e) )
		return [ False, { 'error' : str(e) } ]
	logger.debug('------------------------ END prendiS3ImgBoto3 -------------- ')
	return filename





def importaImgFromAws( fileS3Url, section, titolo ):
	logger.info('------------------------ INIT importaImgFromAws -------------- ')
	logger.debug('------------------------ INIT importaImgFromAws -------------- ')
	[ resultBool, binary ] = creaBinaryFromAws( fileS3Url, section, titolo )
	if not resultBool :
		# non son riuscito a fare la load del file ....
		logger.debug ( ' not binary' )
		logger.warning( ' not binary' )
		return [ False , 'not binary ' ]
	else:
		jsonPerImport = {'title':titolo,'section':section, 'oldType' : 'keyframe'}
		[ resultBool, newKeyframe ] = CCType.MasterType( None, None, jsonPerImport )
		if not resultBool:
			return [ False, { 'error' : "in importaImgFromAws non riesco ad creare img" } ]
		newKeyframe.createDocument()
		# per questa non serve ma negli altri 
		# devo chiamare 
		newKeyframe.updateFields( jsonPerImport, newKeyframe.listaFields)
		newKeyframe.sistemaBinary( binary )
		# per il keyframe e' sicuramente published ... per gli altri che settano draft vedremo
		newKeyframe.createState('published')	
		newKeyframe.dumpDoc() 
		#e qui ho lxml prnto da buttare su
		[ resultBool, imageCueId ] = cueServices.createMamStr( section, newKeyframe.getDoc())

	
		if not resultBool:
			return [ False, { 'error' : "in produciKeyframeDaKafka non riesco ad creare img" } ]

		logger.debug('creato Img cone CUE id : ' + str(imageCueId))
	return [ True, imageCueId ]

def creaBinaryFromAws( fileS3Url, section, titolo ):

	logger.info('------------------------ INIT creaBinaryFromAws -------------- ')
	logger.debug('------------------------ INIT creaBinaryFromAws -------------- ')

	resultBool = False
	resultJson = {}
	#section = os.environ['IMPORT_SECTION']
	section = section



	logger.debug(fileS3Url)

	if 'rsiori' in fileS3Url:
		filename = prendiS3ImgBoto3( fileS3Url ) 
		[ resultBool, binary ]  = cueServices.uploadBinaryFromFile( filename, titolo )
	else:
		binData = prendiS3Img( fileS3Url ) 
		[ resultBool, binary ]  = cueServices.uploadBinaryFromBin( binData , titolo)
	
	if not resultBool :
		# non son riuscito a fare la load del file ....
		# continuo senza cambiare img con id
		logger.debug ( ' not binary' )
		logger.warning( ' not binary' )
		return [ False , 'not binary ' ]
	else:
		# ho fatto upload binary e in binary[1] ho la location url del binary
		# da passare alla creazione del content picture
		logger.debug ( ' binary ok ' )
		return [ True, binary ]

	logger.info('------------------------ END creaBinaryFromAws -------------- ')
	logger.debug('------------------------ END creaBinaryFromAws -------------- ')

	return [ False , 'boh ? ' ]

def prendiSectionDaSource( jsonFlatMessage , sectionId ):

	lista = { 'ingest-systems-sonaps':'10630', 
		  'ingest-media':'5',
		  'ingest-systems-cmm':'5',
		  'livelink':'5',
                  'ingest-media-aws':'5'
	}
	result = sectionId
	if 'source' not in jsonFlatMessage:
		logger.debug('source not in jsonFlatMessage')
		return result
	else:
		if jsonFlatMessage['source'].lower() in lista:
			# aggiunta per gestire quelli che arrivano dal livelink
			# che se hanno il valore "radio + web" nel campo diffusion 
			# devono essere buttati nella section 23075
			logger.debug('source in lista')
			if 'livelink' in jsonFlatMessage['source'].lower() and 'diffusion' in jsonFlatMessage and 'radio' in jsonFlatMessage['diffusion']:
				return pySettaVars.sectionMapping['23075']
			else:
				return pySettaVars.sectionMapping[lista[ jsonFlatMessage['source'].lower()] ]

	return result

def prendiSectionId( jsonFlatMessage ):

	logger.debug ( '------------------------ INIT prendiSectionId -------------- ' )
	logger.debug ( '------------------------ INIT prendiSectionId -------------- ' )
	channel = 'la1'
	result = pySettaVars.sectionMapping['15100']
	sectionName = ''
	productTypeDesc = ''

	#logger.debug ( jsonFlatMessage ) 

	if 'channel' in jsonFlatMessage:
		channel = jsonFlatMessage['channel'].lower()
		jsonFlatMessage['__CHANNEL_MAMPROGRAMME__'] = channel
	if '__CHANNEL_MAMPROGRAMME__' in jsonFlatMessage:
		channel = jsonFlatMessage['__CHANNEL_MAMPROGRAMME__'].lower()
	if '__DA_PASSARE_A_BRAND__' in jsonFlatMessage:
		sectionName = jsonFlatMessage['__DA_PASSARE_A_BRAND__']
	if 'editorialContent_brand_title' in jsonFlatMessage:
		sectionName = jsonFlatMessage['editorialContent_brand_title']
	if '__PRODUCTTYPEDESC_MAMPROGRAMME__' in jsonFlatMessage:
		productTypeDesc = jsonFlatMessage['__PRODUCTTYPEDESC_MAMPROGRAMME__']
	if 'sourceSystem_louise_productTypeDescription' in jsonFlatMessage:
		productTypeDesc = jsonFlatMessage['sourceSystem_louise_productTypeDescription']

	print ('channel : ' +  channel )
	print ('sectionName : ' +  sectionName )
	print ('productTypeDesc : ' +  productTypeDesc )

	result = cueServices.getIdServizioSezioni( channel, sectionName, result )
	if not '-1' in result :
		# il servizio sezioni mi ha dato una sezione giusta 
		# la ritorno
		print( 'cueServices.getIdServizioSezioni ha trovato sezione : ' + str(result))
		return result

	# piccolo fix per TG Lis che deve andare nella section 22357 
	# Telegiornale lingua dei segni FIX
	if 'event' in channel:
		if ('Telegiornale Lingua dei segni' in jsonFlatMessage['title'] ) or ( 'TG nella lingua dei segni' in jsonFlatMessage['title']):
			logger.debug('FIX Telegiornale lingua dei segni')
			logger.debug('FIX Telegiornale lingua dei segni')
			return pySettaVars.sectionMapping['22357']
		

	# piccolo fix per Meteo Lis che deve andare nella section 30019 
	# Meteo Lingua dei segni FIX
	if 'event' in channel:
		if ('Meteo Lingua dei segni' in jsonFlatMessage['title'] ) or ( 'Meteo LIS' in jsonFlatMessage['title']):
			logger.debug('FIX Meteo lingua dei segni')
			logger.debug('FIX Meteo lingua dei segni')
			return pySettaVars.sectionMapping['30019']
	

	# metto i valori di default nel caso in cui il servizio di riconoscimento
	# sections mi restituisca 0
	#print ( 'CLAD' )
	print ('channel : ' +  channel )
	print('productTypeDesc' + productTypeDesc)

	if 'la1' in channel:
		#logger.debug( 'passo da la1')
		if 'Telefilm' in productTypeDesc:
			result = pySettaVars.sectionMapping['14779']
		else:
			if 'Film' in productTypeDesc:
				result = pySettaVars.sectionMapping['4127']
			else:
				# questo e id di altri programmi per La1
				result = pySettaVars.sectionMapping['15097']
		
	else:
		#logger.debug( 'passo da la2')
		if 'Telefilm' in productTypeDesc:
			result = pySettaVars.sectionMapping['14782']
		else:
			if 'Film' in productTypeDesc:
				result = pySettaVars.sectionMapping['4553']
			else:
				# questo e id di altri programmi per La2
				result = pySettaVars.sectionMapping['15100']

	#logger.debug ( 'CLAD  ' + result )

	result = cueServices.getIdServizioSezioni( channel, sectionName, result )
	logger.debug ( '------------------------ END prendiSectionId -------------- ' )
	logger.debug ( '------------------------ END prendiSectionId -------------- ' )

	return  result

def prendiTypeDaListaTags( jsonFlatMessage ):
	# giro per trovare che tipo di roba e' per metterlo in type 
	# in modo ch poi la prendiTagsDaJson sa che tipo di tags prendere 
	# se film docu o altro ...
	# e mettere il valore della lista senza type nel campo trafficSystemMetadata_SrgPlayTopics
	# cosi' da poter usare la stessa funzione di sempre per prendere i tags
	logger.debug ( '------------------------ INIT prendiTypeDaListaTags -------------- ' )

	result = jsonFlatMessage
	_tmpdict = []
	_tmpstr = ''

	if ('SrgPlayTopics' in jsonFlatMessage) and (not jsonFlatMessage['SrgPlayTopics'] is None ) and (len(jsonFlatMessage['SrgPlayTopics']) > 0) :
		_tmpstr = 'SrgPlayTopics'
	elif ('trafficSystemMetadata_SrgPlayTopics' in jsonFlatMessage) and (not jsonFlatMessage['trafficSystemMetadata_SrgPlayTopics'] is None ) and (len(jsonFlatMessage['trafficSystemMetadata_SrgPlayTopics']) > 0):
		 _tmpstr = 'trafficSystemMetadata_SrgPlayTopics'
	else:
		result['trafficSystemMetadata_type'] = ''
		result['trafficSystemMetadata_SrgPlayTopics'] = []
		logger.debug ( '------------------------ END prendiTypeDaListaTags -------------- ' )
		return result
		

	tipo = { 'KIDS':'serie-kids', 
		'FILM':'film',
		'TELEFILM': 'telefilm',
		'DOCUMENTARIO':'documentario',
		'DOCUMENTARI':'documentario' }

	for tag in jsonFlatMessage[_tmpstr]:
		if tag in tipo:
			result['trafficSystemMetadata_type'] = tipo[tag]
		elif 'TAG' in tag:
			continue
		else:
			_tmpdict.append( tag )
	result['trafficSystemMetadata_SrgPlayTopics'] = _tmpdict
	logger.debug ( '------------------------ END prendiTypeDaListaTags -------------- ' )

	print(' result trafficSystemMetadata_SrgPlayTopics : ' + str(result['trafficSystemMetadata_SrgPlayTopics']))
	if 'trafficSystemMetadata_type' in result:
		print(' result trafficSystemMetadata_type : ' + str(result['trafficSystemMetadata_type']))
	print ( '------------------------ END prendiTypeDaListaTags -------------- ' )
	return result


def prendiTagsDaJson( jsonToClean ):
	logger.debug ( ' ------------------------ INIT prendiTagsDaJson -------------- ' )
	result = ''
	if not ('trafficSystemMetadata_SrgPlayTopics' in jsonToClean) or not(len(jsonToClean['trafficSystemMetadata_SrgPlayTopics']) > 0):
		logger.debug('Non esiste trafficSystemMetadata_SrgPlayTopics - niente TAGS')
		print('Non esiste trafficSystemMetadata_SrgPlayTopics - niente TAGS')
		print('ESCO')
		return result
	

	# qui arriviamo perche la source era mam-trafficsystem-vod
	# adesso se esiste struttura trafficSystemMetadata 
	tagList = []

	if True:
	#try:

		if 'trafficSystemMetadata_type' in jsonToClean and ( 'Telefilm' in jsonToClean['trafficSystemMetadata_type'] or 'telfilm' in  jsonToClean['trafficSystemMetadata_type'] or 'telefilm' in  jsonToClean['trafficSystemMetadata_type']):
			# in result devo mettere i tags dei Telefilms -- seriealtatensione etc etc
			if 'trafficSystemMetadata_SrgPlayTopics' in jsonToClean and (len(jsonToClean['trafficSystemMetadata_SrgPlayTopics']) > 0):
				for tag in jsonToClean['trafficSystemMetadata_SrgPlayTopics']:
					print('telefilm')
					print(tag)
					if tag in pySettaVars.tagDictTelefilms:
						tagList.append(pySettaVars.tagDictTelefilms[ tag ])
					else:
						logger.warning(' non ho trovato il tag : ' + tag )
		elif 'trafficSystemMetadata_type' in jsonToClean and 'film' in jsonToClean['trafficSystemMetadata_type']:
			# in result devo mettere i tags dei films -- filmaltatensione etc etc
			if 'trafficSystemMetadata_SrgPlayTopics' in jsonToClean and (len(jsonToClean['trafficSystemMetadata_SrgPlayTopics']) > 0):
				for tag in jsonToClean['trafficSystemMetadata_SrgPlayTopics']:
					print('film')
					print(tag)
					if tag in pySettaVars.tagDictFilms:
						tagList.append( pySettaVars.tagDictFilms[ tag ])
					else:
						logger.warning(' non ho trovato il tag : ' + tag )

		elif ('trafficSystemMetadata_type' in jsonToClean ) and (('documentari' in jsonToClean['trafficSystemMetadata_type']) or ('documentario' in jsonToClean['trafficSystemMetadata_type'])):
			# in result devo mettere i tags dei documentari  aggiungendo all'inizio il tag documentari
				logger.debug('passo')
				jsonToClean['trafficSystemMetadata_SrgPlayTopics'].append('DOCUMENTARI')
				for tag in jsonToClean['trafficSystemMetadata_SrgPlayTopics']:
					print('documentari')
					print(tag)
					if tag in pySettaVars.tagDictDocu:
						tagList.append(pySettaVars.tagDictDocu[ tag ])
					else:
						logger.warning(' non ho trovato il tag : ' + tag )
		elif 'trafficSystemMetadata_type' in jsonToClean and 'serie-kids' in jsonToClean['trafficSystemMetadata_type']:
			# in result devo mettere i tags dei documentari -- filmaltatensione etc etc
			if 'trafficSystemMetadata_SrgPlayTopics' in jsonToClean and (len(jsonToClean['trafficSystemMetadata_SrgPlayTopics']) > 0):
				for tag in jsonToClean['trafficSystemMetadata_SrgPlayTopics']:
					print('serie-kids')
					print(tag)
					if tag in pySettaVars.tagDictKids:
						tagList.append(pySettaVars.tagDictKids[ tag ])
					else:
						logger.warning(' non ho trovato il tag : ' + tag )

	'''
	except Exception as e:
		logger.debug ( 'PROBLEMI in prendiTagsDaJson : ' + str(e) )
		logger.warning ( 'PROBLEMI in prendiTagsDaJson : ' + str(e) )
		return []
	'''
	print('tagList : ' + str(tagList))
		
	logger.debug ( '------------------------ END prendiTagsDaJson -------------- ' )
	return tagList


def addRelEditorialKeyframe( assetEceId, keyframeEceId ):

	logger.debug ( '------------------------ INIT addRelEditorialKeyframe -------------- ' )
	logger.debug ( '------------------------ INIT addRelEditorialKeyframe -------------- ' )
	logger.debug ( '- aggiungo EceId : ' + keyframeEceId + ' al EceId : ' + assetEceId )
	logger.info ( '- aggiungo keyframeEceId : ' + keyframeEceId + ' al EceId : ' + assetEceId )
	result = False

	# qui devo aggiungere alle relation di questo programme 
	# l asset eceId
	[ successGetId, resultContent, eTag  ] =  cueServices.getId( assetEceId )
	if not successGetId:
		return [ False, {"error" : "Non trovato CueId di riferimento : " + str(assetEceId) } ]

	#se sono qui ho il resultContent e posso prenderlgi sopr un piccoloParser
	xmlServToUpdate = xmlService.xmlPiccoloParser( resultContent )

	editorialLink = xmlServToUpdate.creaRelationKeyframe( keyframeEceId, True )
	thumbnailLink = xmlServToUpdate.creaRelationThumbnail( keyframeEceId )
	listaRelated = xmlServToUpdate.prendiListaRelated('related' ) 
	# in listaRelated ho la liste delle relazioni di questo asset
	#logger.debug ( ordinaEditorial( listaRelated ) )
	xmlServToUpdate.rimuoviListaRelated( 'related' )
	xmlServToUpdate.aggiungiEditorialList( editorialLink,thumbnailLink, listaRelated ) 

	# prendo lo stato dell asset 
	stato = xmlServToUpdate.getState( )
	print("stato : " + stato)
	# nel caso sia deleted esco
	if 'deleted' in stato:
		return [ False, {"error" : "l' EceId di riferimento e stato cancellato" } ]

	xmlServToUpdate.cambiaState( stato )


	xmlServToUpdate.dumpDoc()
	#exit(0)
	nome_file = creaNomeFile( 'keyframe' )
	xmlServToUpdate.writeToFile(nome_file)
	result = cueServices.putIdeTag(assetEceId, nome_file, eTag)

	logger.debug ( '------------------------ END addRelEditorialKeyframe -------------- ' )
	logger.debug ( '------------------------ END addRelEditorialKeyframe -------------- ' )
	return result

def verificaUpdateProgramme( tree, eceId ):
	logger.debug( '------------------------ INIT verificaUpdateProgramme -------------- ' )
	logger.debug( '------------------------ INIT verificaUpdateProgramme -------------- ' )
	result = False
	idFromLead = -1
		
	# devo prendere l identifier della relazione in lead 
	idFromLead = prendiLeadId( tree, 'related')


	# e quindi vedere se e diversa da eceId
	if eceId in idFromLead:
		logger.debug(' stesso id nel lead non faccio nulla' )
		logger.debug(' stesso id nel lead non faccio nulla' )
	else:
		logger.debug(' id diversi metto eceId = ' + eceId + ' in cima alle lead')
		logger.debug(' id diversi metto eceId = ' + eceId + ' in cima alle lead')
		return True

	logger.debug( '------------------------ END verificaUpdateProgramme -------------- ' )
	logger.debug( '------------------------ END verificaUpdateProgramme -------------- ' )
	return result



def prendiSectionDaTraffic( jsonFlatMessage , sectionId ):

	logger.debug ( '------------------------ INIT prendiSectionDaTraffic -------------- ' )
	result = sectionId
	if 'source' not in jsonFlatMessage :
		logger.debug('source not in jsonFlatMessage')
		return result
	else:

		if 'mam-trafficsystem-vod' in jsonFlatMessage['source'].lower() and 'trafficSystemMetadata_hasSubtitlesLIS' in jsonFlatMessage and ( jsonFlatMessage['trafficSystemMetadata_hasSubtitlesLIS'] ):
			# devo chiamare il servizio di Ivan
			# aggiungendo -lis in fondo al nome

			if 'trafficSystemMetadata_web_TITPRESSSERIE' in jsonFlatMessage and (len(jsonFlatMessage['trafficSystemMetadata_web_TITPRESSSERIE'] ) > 0) :
				sectionName = jsonFlatMessage['trafficSystemMetadata_web_TITPRESSSERIE'] + '-lis'
				channel = jsonFlatMessage['channel']
				# DEBUG MANCA cueServices.getIdServizioSezioni
				result = cueServices.getIdServizioSezioni( channel, sectionName, result )
				logger.debug(result)
				logger.debug ( '------------------------ END prendiSectionDaTraffic -------------- ' )
				return result

		elif 'mam-trafficsystem-vod' in jsonFlatMessage['source'].lower() and 'trafficSystemMetadata_type' in jsonFlatMessage and ( 'Telefilm' in jsonFlatMessage['trafficSystemMetadata_type'] or 'telfilm' in jsonFlatMessage['trafficSystemMetadata_type'] or 'telefilm' in jsonFlatMessage['trafficSystemMetadata_type'] ):
			# devo chiamare il servizio di Ivan
			# qui devo prendere il campo trafficSystemMetadata_web_TITPRESSSERIE dove trovo la 
			# chiave per il mapping

			if 'trafficSystemMetadata_web_TITPRESSSERIE' in jsonFlatMessage and len(jsonFlatMessage['trafficSystemMetadata_web_TITPRESSSERIE'] ) > 0 :
				sectionName = jsonFlatMessage['trafficSystemMetadata_web_TITPRESSSERIE']
				channel = jsonFlatMessage['channel']
				# DEBUG MANCA cueServices.getIdServizioSezioni
				result = cueServices.getIdServizioSezioni( channel, sectionName, result )
				logger.debug(result)
				logger.debug ( '------------------------ END prendiSectionDaTraffic -------------- ' )
				return result

		elif 'mam-trafficsystem-vod' in jsonFlatMessage['source'].lower() and 'trafficSystemMetadata_type' in jsonFlatMessage and 'serie-kids' in jsonFlatMessage['trafficSystemMetadata_type']:
			# se e un serie-kids e ha i tags dei bimbi deve andare nella 16756
			if ('trafficSystemMetadata_SrgPlayTopics' in jsonFlatMessage) and not (jsonFlatMessage['trafficSystemMetadata_SrgPlayTopics'] is None) and ( len(jsonFlatMessage['trafficSystemMetadata_SrgPlayTopics']) > 0 ) and ( 'KIDS' in jsonFlatMessage['trafficSystemMetadata_SrgPlayTopics'] or 'PICCOLI' in jsonFlatMessage['trafficSystemMetadata_SrgPlayTopics'] or 'GRANDI' in jsonFlatMessage['trafficSystemMetadata_SrgPlayTopics']):
	
				if 'trafficSystemMetadata_web_TITPRESSSERIE' in jsonFlatMessage and len(jsonFlatMessage['trafficSystemMetadata_web_TITPRESSSERIE'] ) > 0 :
					sectionName = jsonFlatMessage['trafficSystemMetadata_web_TITPRESSSERIE']
					channel = jsonFlatMessage['channel']
					# DEBUG MANCA cueServices.getIdServizioSezioni
					result = cueServices.getIdServizioSezioni( channel, sectionName, result )
					logger.debug(result)
					return result

		elif 'mam-trafficsystem-vod' in jsonFlatMessage['source'].lower() and ('trafficSystemMetadata_type' in jsonFlatMessage and ('documentari' in jsonFlatMessage['trafficSystemMetadata_type'])):
			# se e un documentario deve andare nella 23093
			if 'trafficSystemMetadata_web_TITPRESSSERIE' in jsonFlatMessage and (len(jsonFlatMessage['trafficSystemMetadata_web_TITPRESSSERIE'] ) > 0 ):
				sectionName = jsonFlatMessage['trafficSystemMetadata_web_TITPRESSSERIE']
				channel = jsonFlatMessage['channel']
				# DEBUG MANCA cueServices.getIdServizioSezioni
				result = cueServices.getIdServizioSezioni( channel, sectionName, result )
				logger.debug(result)
				return result
			else:
				return pySettaVars.sectionMapping['23093']

		elif 'mam-trafficsystem-vod' in jsonFlatMessage['source'].lower() and 'trafficSystemMetadata_type' in jsonFlatMessage and 'film' in jsonFlatMessage['trafficSystemMetadata_type']:
			# se e un film e ha i tags dei bimbi deve andare nella 16756
			if ('trafficSystemMetadata_SrgPlayTopics' in jsonFlatMessage) and not (jsonFlatMessage['trafficSystemMetadata_SrgPlayTopics'] is None) and ( len(jsonFlatMessage['trafficSystemMetadata_SrgPlayTopics']) > 0  ) and ( 'KIDS' in jsonFlatMessage['trafficSystemMetadata_SrgPlayTopics'] or 'PICCOLI' in jsonFlatMessage['trafficSystemMetadata_SrgPlayTopics'] or 'GRANDI' in jsonFlatMessage['trafficSystemMetadata_SrgPlayTopics']):
	
				if 'trafficSystemMetadata_web_TITPRESSSERIE' in jsonFlatMessage and len(jsonFlatMessage['trafficSystemMetadata_web_TITPRESSSERIE'] ) > 0 :
					sectionName = jsonFlatMessage['trafficSystemMetadata_web_TITPRESSSERIE']
					channel = jsonFlatMessage['channel']
					# DEBUG MANCA cueServices.getIdServizioSezioni
					result = cueServices.getIdServizioSezioni( channel, sectionName, result )
					logger.debug(result)
					return result

			# altrimenti deve andare nella section 28635
			else:
				logger.debug ( '------------------------ END prendiSectionDaTraffic -------------- ' )
				return pySettaVars.sectionMapping['28635']

	logger.debug ( '------------------------ END prendiSectionDaTraffic -------------- ' )
	return result

def getEceIdFromCmsJson( cmsJson ):
	logger.debug ( '------------------------ inizia getEceIdFromCmsJson -------------- ' )
	logger.debug ( '------------------------ inizia getEceIdFromCmsJson -------------- ' )
	result=[ None, None ]

	try:
		# prendo Ece id dal json
		# "urn":"urn:rsi:escenic:

		if  not 'urn' in cmsJson or len(cmsJson['urn']) < 17:
			logger.debug ( 'in getEceIdFromCmsJson non esiste cms[urn]')
			logger.debug ( 'in getEceIdFromCmsJson non esiste cms[urn]')
			return [ None, None ]
		
		if 'urn' in cmsJson and 'livestreaming' in cmsJson['urn'] :
			logger.debug ( 'in getEceIdFromCmsJson e un livestreaming non lo metto nel lead di nessuno')
			logger.debug ( 'in getEceIdFromCmsJson e un livestreaming non lo metto nel lead di nessuno')
			return [ None, None ]

		eceId = cmsJson['urn'].split(':')[-1]
		
		[ successGetId, resultContent  ] = cueServices.getId( eceId )
		if not successGetId:
			return [ False, {'error':'cueServices.getId non andato a buon fine'} ]

	except urllib.error.HTTPError as e:
		logger.debug(' EXCEPTIOOOONNNNNN - ritorno none !!!! ')
		return [ False, {'error': str(e)} ]

	logger.debug ( '------------------------ END getEceIdFromCmsJson -------------- ' )
	logger.debug ( '------------------------ END getEceIdFromCmsJson -------------- ' )

	return [ True, resultContent ]

def getProgrammeIdFromCmsJson( cmsJson ):
	logger.debug ( '------------------------ inizia getProgrammeIdFromCmsJson -------------- ' )
	logger.debug ( '------------------------ inizia getProgrammeIdFromCmsJson -------------- ' )
	result=[ None, None ]

	try:
		# prendo Programme id dal json
		# "urn":"urn:rsi:escenic:

		if  not 'urn' in cmsJson or len(cmsJson['urn']) < 17:
			logger.debug ( 'in getProgrammeIdFromCmsJson non esiste cms[urn]')
			logger.debug ( 'in getProgrammeIdFromCmsJson non esiste cms[urn]')
			return [ None, None ]

		eceId = cmsJson['urn'].split(':')[-1]
		[ successGetId, resultContent  ] = cueServices.getId( eceId )
		if not successGetId:
			return [ False, {'error':'cueServices.getId non andato a buon fine'} ]

	except urllib.error.HTTPError as e:
		logger.debug(' EXCEPTIOOOONNNNNN - ritorno none !!!! ')
		return [ None, None ]

	logger.debug ( '------------------------ END getProgrammeIdFromCmsJson -------------- ' )
	logger.debug ( '------------------------ END getProgrammeIdFromCmsJson -------------- ' )

	return [ True, resultContent ]

def radioProgrammaJson( messageJson ):
	logger.debug ( '------------------------ INIT radioProgrammaJson -------------- ' )

	result = messageJson

	if 'title' in messageJson:
		messageJson['editorialContent_titlePress'] = messageJson['title']

	if 'startTime' in messageJson:
		timestamp = int(messageJson['startTime'])/1000.0
		logger.debug( timestamp )
		value = datetime.utcfromtimestamp(timestamp)
		data = value.strftime("%Y-%m-%dT%H:%M:%SZ")
		logger.debug( data )
		messageJson['dateTimes_startBroadcastPress'] = data

	if 'body' in messageJson:
		messageJson['editorialContent_longDescriptionPress'] = messageJson['body']
	else:
		messageJson['editorialContent_longDescriptionPress'] = ''

	if 'leadText' in messageJson:
		messageJson['editorialContent_shortDescriptionPress'] = messageJson['leadText']
	else:
		messageJson['editorialContent_shortDescriptionPress'] = ''
		messageJson['editorialContent_show_title'] = messageJson['series']
		messageJson['episode_legacyid'] = 'episode_legacyid'
		messageJson['episode_episodenr'] = 'episode_episodenr'

	if 'published' in messageJson:
		messageJson['__STATE_MAMPROGRAMME__'] = 'published' if messageJson['published']  else 'draft'
	logger.debug (messageJson)

	logger.debug ( '------------------------ END radioProgrammaJson -------------- ' )

	return result
	
def preparaJsonRelationProgramme(  eceId,flatMsg, sectionId ):
	result = {}

	tmpjson = pySettaVars.fieldsRelationPerGiu

	for key,value in tmpjson.items() :
		if value in flatMsg:
			result[ key ] = flatMsg[ value ] 
	result['cue'] = int(eceId)
	result['SectionId'] = int(sectionId)
	logger.debug ( result )
	logger.debug( 'json per Giu :: ' + str( result ))

	return result

	

def aggiungiDelta( pubDateStr, daAggiungere ):
	# in pubDateStr ho roba tipo <updated>2022-03-01T23:00:00Z</updated>
	# in daAggiungere ho un deltaTime
	
	# tolgo capo e coda
	pubDateStr = pubDateStr[9:-10]
	# aggiungo il delta
	_tmpDate = datetime.strptime( pubDateStr,'%Y-%m-%dT%H:%M:%SZ' ) + daAggiungere
	# ricreo la stringa
	pubDateStr = '<updated>' + datetime.strftime( _tmpDate, '%Y-%m-%dT%H:%M:%SZ') + '</updated>'
	return pubDateStr


def creaRelationDataProgramme( eceId, flatMsg, sectionId ):
	result = {}
	# deve creare un json come questo:
	#testData = {"urn":"rsi:mam:9ea7cdb0142fef040426ebbddb41b296",
		#"cms":{
		#"urn":"rsi:cue:12682029"
		##},
		#"sourceSystem":{
		#"urn":"rsi:mp:102867428"
		#}
	#}
	#testChiave = "rsi:mam:9ea7cdb0142fef040426ebbddb41b296-rsi:cue:12682029" 

	jsonPerGiu = preparaJsonRelationProgramme( eceId, flatMsg, sectionId )
	
	aggiuntaRotturadiCazzo = 'rundown'
	if 'Video' in flatMsg['contentType']:
		aggiuntaRotturadiCazzo = 'video'
	elif 'Audio' in  flatMsg['contentType']:
		aggiuntaRotturadiCazzo = 'audio'
	elif 'livestreaming' in  flatMsg['contentType']:
		aggiuntaRotturadiCazzo = 'livestreaming'
	elif 'programme' in  flatMsg['contentType']:
		 flatMsg['contentType'] = 'video'

	if 'source' in flatMsg and 'RadioProgramma' in  flatMsg['source']:
		aggiuntaRotturadiCazzo = 'radioprogramma'
	 
	if 'sourceSystem_urn' in flatMsg:
		result = { "chiave" : flatMsg['urn'] + "-" + "rsi:cue:"   + flatMsg['contentType'] + ':' + eceId,
			   "value" : { "urn":flatMsg['urn'],
					"cms" :  {
						"urn":"rsi:cue:"   + flatMsg['contentType'] + ':' + eceId ,
						"content": jsonPerGiu,
					},
					"sourceSystem":{ 
					"urn":flatMsg[ 'sourceSystem_urn' ]
					}
				}
			}
	else:
		result = { "chiave" : flatMsg['urn'] + "-" + "rsi:cue:"  + flatMsg['contentType'] + ':' + eceId,
			   "value" : { "urn":flatMsg['urn'],
					"cms" :  {
						"urn":"rsi:cue:" + flatMsg['contentType'] + ':' + eceId ,
						"content": jsonPerGiu
					},
				}
			}

	logger.debug( 'relationData :: ' + str( result ) )
	logger.debug( 'relationData :: ' + str(result ) )
	
	return result



def sistemaPublishForLivelink( jsonToClean ):
	
	result =  jsonToClean
	
	if 'source' in jsonToClean and 'livelink' in jsonToClean['source'].lower():
		# devo mettere la publishdate = markin della clip
		if 'clips' in jsonToClean and len ( jsonToClean['clips'] ) > 0:
			clipsValues = jsonToClean['clips'][0]
			if 'markIn' in clipsValues :
				result['playMarkIn'] = trasformaMIn( clipsValues['markIn'] )

				result['__ECE_UPDATED__'] = '<updated>' +  prendiDataDaMin( clipsValues['markIn'] )  + '</updated>'
		else:
			logger.debug('arriva da livelink ma non ho trovato la clip per settare la publishdate !' )
			logger.warning('arriva da livelink ma non ho trovato la clip per settare la publishdate !' )

	return result

def sistemaLiveDates( result, jsonToClean ):
		
	logger.debug ( '------------------------ INIT sistemaLiveDates -------------- ' )
	#logger.debug( jsonToClean )
	# e aggiungo tutta la trattazione dello starttime
	if 'streamingStartTime' in jsonToClean and len(str(jsonToClean['streamingStartTime'] )) > 0:
		jsonToClean['streamingStartTime'] = str(jsonToClean['streamingStartTime'])
		if 'Z' in jsonToClean['streamingStartTime']:
			logger.debug( 'arrivata streamingStartTime dal Programme' )
			# mi e' arrivata la data gia nel formato giusto
			data = jsonToClean['streamingStartTime']
			logger.debug( data )
		else :
			logger.debug( 'trovato streamingStartTime' )
			timestamp = int(jsonToClean['streamingStartTime'])/1000.0
			if timestamp < 0:
				print('Mi e arrivato rimestamp < 0 ' )
				data = ''
			else:
				print( timestamp )
				value = datetime.utcfromtimestamp(timestamp)
				data = value.strftime("%Y-%m-%dT%H:%M:%SZ")
				print( data )
		result['streamingStartTime'] = data
	else:
		result['streamingStartTime'] = ''


	# e aggiungo tutta la trattazione dello endtime
	if 'streamingEndTime' in jsonToClean and len(str(jsonToClean['streamingEndTime'] )) > 0:
		jsonToClean['streamingEndTime'] = str(jsonToClean['streamingEndTime'])
		if 'Z' in jsonToClean['streamingEndTime']:
			logger.debug( 'arrivata streamingEndTime dal Programme' )
			# mi e' arrivata la data gia nel formato giusto
			data = jsonToClean['streamingEndTime']
			logger.debug( data )
		else :
			logger.debug( 'trovato streamingEndTime' )
			timestamp = int(jsonToClean['streamingEndTime'])/1000.0
			if timestamp < 0:
				print('Mi e arrivato rimestamp < 0 ' )
				data = ''
			else:
				print( timestamp )
				value = datetime.utcfromtimestamp(timestamp)
				data = value.strftime("%Y-%m-%dT%H:%M:%SZ")
				print( data )
		result['streamingEndTime'] = data
	else:
		result['streamingEndTime'] = ''


	# e aggiungo tutta la trattazione dello socialStart
	if 'socialStart' in jsonToClean and len(str(jsonToClean['socialStart'])) > 0:
		jsonToClean['socialStart'] = str(jsonToClean['socialStart'])
		if 'Z' in jsonToClean['socialStart']:
			logger.debug( 'arrivata socialStart dal Programme' )
			# mi e' arrivata la data gia nel formato giusto
			data = jsonToClean['socialStart']
			logger.debug( data )
		else :
			logger.debug( 'trovato socialStart' )
			timestamp = int(jsonToClean['socialStart'])/1000.0
			if timestamp < 0:
				print('Mi e arrivato rimestamp < 0 ' )
				data = ''
			else:
				print( timestamp )
				value = datetime.utcfromtimestamp(timestamp)
				data = value.strftime("%Y-%m-%dT%H:%M:%SZ")
				print( data )
		result['socialStart'] = data
	else:
		result['socialStart'] = ''


	# e aggiungo tutta la trattazione dello socialEnd
	if 'socialEnd' in jsonToClean and len(str(jsonToClean['socialEnd'])) > 0:
		jsonToClean['socialEnd'] = str(jsonToClean['socialEnd'])
		if 'Z' in jsonToClean['socialEnd']:
			logger.debug( 'arrivata socialEnd dal Programme' )
			# mi e' arrivata la data gia nel formato giusto
			data = jsonToClean['socialEnd']
			logger.debug( data )
		else :
			logger.debug( 'trovato socialEnd' )
			timestamp = int(jsonToClean['socialEnd'])/1000.0
			if timestamp < 0:
				print('Mi e arrivato rimestamp < 0 ' )
				data = ''
			else:
				print( timestamp )
				value = datetime.utcfromtimestamp(timestamp)
				data = value.strftime("%Y-%m-%dT%H:%M:%SZ")
				print( data )
		result['socialEnd'] = data
	else:
		result['socialEnd'] = ''

	# e aggiungo tutta la trattazione dello eventTime
	if 'eventTime' in jsonToClean and len(str(jsonToClean['eventTime'])) > 0:
		jsonToClean['eventTime'] = str(jsonToClean['eventTime'])
		if 'Z' in jsonToClean['eventTime']:
			logger.debug( 'arrivata eventTime dal Programme' )
			# mi e' arrivata la data gia nel formato giusto
			data = jsonToClean['eventTime']
			logger.debug( data )
		else :
			logger.debug( 'trovato eventTime' )
			timestamp = int(jsonToClean['eventTime'])/1000.0
			if timestamp < 0:
				print('Mi e arrivato rimestamp < 0 ' )
				data = ''
			else:
				print( timestamp )
				value = datetime.utcfromtimestamp(timestamp)
				data = value.strftime("%Y-%m-%dT%H:%M:%SZ")
				print( data )
		result['eventTime'] = data
	else:
		result['eventTime'] = ''

	# e aggiungo tutta la trattazione del expire time
	if 'rights_expireDate' in jsonToClean and not 'null' in jsonToClean['rights_expireDate'] and len( jsonToClean['rights_expireDate']) > 0 :
		if 'Z' in jsonToClean['rights_expireDate']:
			logger.debug( 'arrivata rights_expireDate dal Programme' )
			# mi e' arrivata la data gia nel formato giusto
			data = jsonToClean['rights_expireDate'] 
			logger.debug( data )
		else:
			logger.debug( 'trovato rights_expireDate' )
			timestamp = int(jsonToClean['rights_expireDate'])/1000.0
			logger.debug( timestamp )
			value = datetime.utcfromtimestamp(timestamp)
			data = value.strftime("%Y-%m-%dT%H:%M:%SZ")
			logger.debug( data )
		result['__ECE_AGE_EXPIRES__'] = '<age:expires>' + data  + '</age:expires>'
	else:
		result['__ECE_AGE_EXPIRES__'] = ''

	logger.debug ( '------------------------ END sistemaLiveDates -------------- ' )
	return result


def creaExtraStream( jsonToClean ):
	result = ' <vdf:list> '

	# devo creare la lista  tipo 
	#' <vdf:list> <vdf:payload> <vdf:field name="webextraStream"> <vdf:value>https://srgssrrcdvr13ch-lh.akamaihd.net/i/enc13rcdvr_ch@351664/master.m3u8?dw=0</vdf:value> </vdf:field> </vdf:payload> <vdf:payload> <vdf:field name="webextraStream"> <vdf:value>http://srgssrrcdvr13ch-lh.akamaihd.net/z/enc13rcdvr_ch@351664/manifest.f4m</vdf:value> </vdf:field> </vdf:payload> </vdf:list> '

	# e adesso per ogni pezzo di lista devo fare un payload
	if 'hlsURL' in jsonToClean and len(jsonToClean['hlsURL']) > 0:
		result = result + ' <vdf:payload> <vdf:field name="webextraStream"> <vdf:value>' +  jsonToClean['hlsURL'] + '</vdf:value></vdf:field> </vdf:payload> '

	if 'hdsURL' in jsonToClean and len(jsonToClean['hdsURL']) > 0:
		result = result + ' <vdf:payload> <vdf:field name="webextraStream"> <vdf:value>' +  jsonToClean['hdsURL'] + '</vdf:value></vdf:field> </vdf:payload> '
	
	
	result = result + ' </vdf:list> '
	return result

	
def sistemaRightsDates( result, jsonToClean ):
	
	logger.debug ( '------------------------ INIT sistemaRightsDates -------------- ' )
	# e aggiungo tutta la trattazione dello starttime
	if 'rights_activationDate' in jsonToClean and not 'null' in jsonToClean['rights_activationDate'] and len(jsonToClean['rights_activationDate'] ) > 0:
		if 'Z' in jsonToClean['rights_activationDate']:
			logger.debug( 'arrivata rights_activationDate dal Programme' )
			# mi e' arrivata la data gia nel formato giusto
			data = jsonToClean['rights_activationDate']
			logger.debug( data )
		else :
			logger.debug( 'trovato rights_activationDate' )
			timestamp = int(jsonToClean['rights_activationDate'])/1000.0
			logger.debug( timestamp )
			value = datetime.utcfromtimestamp(timestamp)
			data = value.strftime("%Y-%m-%dT%H:%M:%SZ")
			logger.debug( data )
		result['__ECE_UPDATED__'] = '<updated>' + data  + '</updated>'
		result['updated'] = data
		result['__ECE_DCTERMS_AVAILABLE__'] = '<dcterms:available>' + data  + '</dcterms:available>'
		result['dcterms:available'] = data
		result['mediaactivedate'] = data
		# FIX per data sballata
		if (len(result['mediaactivedate'])) > 20:
			result['mediaactivedate'] = result['mediaactivedate'][0:19] + 'Z'
	else:
		result['__ECE_UPDATED__'] = ''
		result['updated'] = ''
		result['__ECE_DCTERMS_AVAILABLE__'] = ''
		result['dcterms:available'] = ''

	# e aggiungo tutta la trattazione del expire time
	if 'rights_expireDate' in jsonToClean and not 'null' in jsonToClean['rights_expireDate'] and len( jsonToClean['rights_expireDate']) > 0 :
		if 'Z' in jsonToClean['rights_expireDate']:
			logger.debug( 'arrivata rights_expireDate dal Programme' )
			# mi e' arrivata la data gia nel formato giusto
			data = jsonToClean['rights_expireDate'] 
			logger.debug( data )
		else:
			logger.debug( 'trovato rights_expireDate' )
			timestamp = int(jsonToClean['rights_expireDate'])/1000.0
			logger.debug( timestamp )
			value = datetime.utcfromtimestamp(timestamp)
			data = value.strftime("%Y-%m-%dT%H:%M:%SZ")
			logger.debug( data )

		result['__ECE_AGE_EXPIRES__'] = '<age:expires>' + data  + '</age:expires>'
		result['age:expires'] = data
		result['mediaexpiredate'] = data
		# FIX per data sballata
		if (len(result['mediaexpiredate'])) > 20:
			result['mediaexpiredate'] = result['mediaexpiredate'][0:19] + 'Z'
		

	return result

def getDurationFromAws( awsJson ):
	result = ''
	if 'transcodedAssets' in awsJson and len(awsJson['transcodedAssets']) > 0 :
		result = awsJson['transcodedAssets'][0]['duration']
		result = str(int(result))
	else:
		result = ''

	return result



def getDurationFromTv( tVJson ):
	result = ''
	if 'variants' in tVJson and len(tVJson['variants']) > 0 :
		result = tVJson['variants'][0]['duration']
		result = str(int(result)/1000.0)

	return result

def prendiTimestamps( listaRel ):

	#logger.debug (listaRel)
	result = []
	for entry in listaRel:
		if (len(entry.attrib['title'])) == 46:
			logger.debug (entry.attrib['title'].split('_')[0])
			logger.debug (str(len(entry.attrib['title'].split('_')[0])))
			if (len(entry.attrib['title'].split('_')[0])) == 13:
				# molto probabile che appendiamo al risultato un timestamp
				# arrivando sempre un titolo nella forma timeStamp_mamId
				# tipo : 1600435699534_622d16064978431175c2e248ccbd36a6
				result.append( entry.attrib['title'].split('_')[0] )

	return result

def trasformaMIn( mIn ):
	result = None
	# questa deve  calcolare il tc_offset dal markIn
	millis = int(mIn)/1000
	seconds=(millis/1000)%60
	seconds = int(seconds)
	minutes=(millis/(1000*60))%60
	minutes = int(minutes)
	hours=(millis/(1000*60*60))%24
	milliseconds = int((int(mIn)%1000)/100)

	logger.debug ("%d:%d:%d.%d" % (hours, minutes, seconds,milliseconds))

	result =  "%d:%d:%d.%d" % (hours, minutes, seconds,milliseconds)

	return result


def esisteTimeStamp( jsonToClean, timeStamp ):
	result = False
	
	
	if 'kTimeStamp' in jsonToClean and timeStamp in jsonToClean['kTimeStamp']:
		logger.debug( timeStamp, jsonToClean['kTimeStamp'] )
		return True

	return result


def timecode_to_milliseconds(timecode):
	# by chatGpt 3.5
	try:
		hours, minutes, seconds = map(int, timecode.split(":"))
		total_milliseconds = (hours * 3600 + minutes * 60 + seconds) * 1000
		return total_milliseconds
	except ValueError:
		return "Formato del timecode non valido. Assicurati di utilizzare il formato HH:MM:SS."


def trasformaTcOffset( mIn ):

	logger.debug( mIn )

	result = None
	# questa deve  calcolare il tc_offset dal markIn
	millis = int(mIn)
	#logger.debug ( 'millis' )
	#logger.debug ( millis )
	hours = (int((millis/(1000*60*60))))
	#hours=(millis/(1000*60*60))%24
	millis = millis - hours * ( 1000*60*60)
	hours= int(hours)
	seconds=(millis/1000)%60
	seconds = int(seconds)
	minutes=(millis/(1000*60))%60
	minutes = int(minutes)
	#logger.debug(hours)
	#logger.debug(minutes)
	#logger.debug(seconds)

	milliseconds = millis - (seconds * 1000 + minutes * 1000 * 60 )
	# contanto che stiamo andando a 25 fps
	# e quindi ci vogliono 40 millisecond per frame
	#logger.debug( 'milliseconds' )
	#logger.debug( milliseconds )
	frames = int(milliseconds/40)
	#logger.debug('frames')
	#logger.debug(frames)

	logger.debug ("%02d:%02d:%02d:%02d" % (hours, minutes, seconds,frames))
	result =  "%02d:%02d:%02d:%02d" % (hours, minutes, seconds,frames)

	return result

def calcolaMilliDuration( mIn, mOut ):
	result = None
	# questa deve  calcolare la duration dati in e out
	result = int(mOut) - int(mIn)
	result = str( result )
	return result



def calcolaDuration( mIn, mOut ):
	result = None
	# questa deve  calcolare la duration dati in e out
	result = int(mOut) - int(mIn)
	result = result / 1000
	result = str( result )
	return result

def creaRelationData( cueId, flatMsg ):
	result = {}
	# deve creare un json come questo:
	#testData = {"urn":"rsi:mam:9ea7cdb0142fef040426ebbddb41b296",
		#"cms":{
		#"urn":"rsi:cue:12682029"
		##},
		#"sourceSystem":{
		#"urn":"rsi:mp:102867428"
		#}
	#}
	#testChiave = "rsi:mam:9ea7cdb0142fef040426ebbddb41b296-rsi:cue:12682029" 
	aggiuntaRotturadiCazzo = 'rundown'
	if 'videosegment' in flatMsg['oldType'] and len(flatMsg['oldType']) == len('videosegment') :
		aggiuntaRotturadiCazzo = 'videosegment'
	elif ('video' in flatMsg['oldType'] and  len(flatMsg['oldType']) == len('video') ) or ('Video' in  flatMsg['oldType'] ) :
		aggiuntaRotturadiCazzo = 'video'
	elif 'audiosegment' in flatMsg['oldType'] and len(flatMsg['oldType']) == len('audiosegment') :
		aggiuntaRotturadiCazzo = 'audiosegment'
	elif 'audio' in  flatMsg['oldType'] or 'Audio' in  flatMsg['oldType']:
		aggiuntaRotturadiCazzo = 'audio'
	elif 'livestreaming' in  flatMsg['oldType']:
		aggiuntaRotturadiCazzo = 'livestreaming'
	

	# per risolvere qualunque rottura di mamUrn o urn io li copio una dentro l'altra 
	if 'mamUrn' in flatMsg and not('urn' in flatMsg):
		flatMsg['urn'] = flatMsg['mamUrn']
	if 'urn' in flatMsg and not('mamUrn' in flatMsg):
		flatMsg['mamUrn'] = flatMsg['urn']

		
	 
	if 'sourceSystem_urn' in flatMsg:
		result = { "chiave" : flatMsg['urn'] + "-" + "rsi:cue:"   +  aggiuntaRotturadiCazzo + ':' + cueId,
			   "value" : { "urn":flatMsg['urn'],
					"cms" :  {
						"urn":"rsi:cue:"   + aggiuntaRotturadiCazzo + ':' + cueId 
					},
					"sourceSystem":{ 
					"urn":flatMsg[ 'sourceSystem_urn' ]
					}
				}
			}
	else:
		result = { "chiave" : flatMsg['urn'] + "-" + "rsi:cue:"  + aggiuntaRotturadiCazzo + ':' + cueId,
			   "value" : { "urn":flatMsg['urn'],
					"cms" :  {
						"urn":"rsi:cue:" + aggiuntaRotturadiCazzo + ':' + cueId 
					},
				}
			}

	print( 'relationData :: ' + str( result ) )
	logger.debug( 'relationData :: ' + str(result ) )
	
	return result

def singleQuoteToDoubleQuote__OLD(singleQuoted):
        '''
        convert a single quoted string to a double quoted one
        Args:
        singleQuoted(string): a single quoted string e.g. {'cities': [{'name': "Upper Hell's Gate"}]}
        Returns:
        string: the double quoted version of the string e.g.
        see
        - https://stackoverflow.com/questions/55600788/python-replace-single-quotes-with-double-quotes-but-leave-ones-within-double-q
        '''
        #singleQuoted = singleQuoted.replace('\"','\\\"')
        #logger.debug(singleQuoted)
        result = ''

        cList=list(singleQuoted)
        inDouble=False;
        inSingle=False;
        for i,c in enumerate(cList):
                #logger.debug ("%d:%s %r %r" %(i,c,inSingle,inDouble))
                if c=="'":
                        if not inDouble:
                                inSingle=not inSingle
                                cList[i]='"'
                elif c=='"':
                        if inSingle:
                                cList[i]='\\\"'
                        inDouble=not inDouble
                doubleQuoted="".join(cList)

        replaceItems = {'None': 'null',
			'False,': 'false,',
			'False}': 'false}' ,
			'True,': 'true,',
			'True}': 'true}'}

        rep = dict((re.escape(k), v) for k, v in replaceItems.items())
        pattern = re.compile("|".join(rep.keys()))
        result = pattern.sub(lambda m: rep[re.escape(m.group(0))], doubleQuoted)
        logger.debug(result)
        exit(0)
        #doubleQuoted = doubleQuoted.replace('None', 'null')
        #doubleQuoted = doubleQuoted.replace('False,', 'false,')
        #doubleQuoted = doubleQuoted.replace('True,', 'true,')
        return result

def singleQuoteToDoubleQuote( singleQuoted):
	logger.debug( '------------ INIT ----------singleQuoteToDoubleQuote ---------------------')
	'''
	convert a single quoted string to a double quoted one
	Args:
	singleQuoted(string): a single quoted string e.g. {'cities': [{'name': "Upper Hell's Gate"}]}
	Returns:
	string: the double quoted version of the string e.g. 
	see
	- https://stackoverflow.com/questions/55600788/python-replace-single-quotes-with-double-quotes-but-leave-ones-within-double-q 
	'''
	result = ''


	apostrofo =  '\\\'' 
	SQ = singleQuoted.replace(apostrofo,'_XXXX_')

	#singleQuoted = singleQuoted.replace('\"','\\\"')
	#logger.debug(singleQuoted)

	#cList=list(singleQuoted)
	cList=list(SQ)
	inDouble=False;
	inSingle=False;
	for i,c in enumerate(cList):
		#logger.debug ("%d:%s %r %r" %(i,c,inSingle,inDouble))
		if c=="'":
			if not inDouble :
				inSingle=not inSingle
				cList[i]='"'
		elif c=='"':
			if inSingle:
				cList[i]='\\\"'
			inDouble=not inDouble
		doubleQuoted="".join(cList)    

	replaceItems = {'None': 'null',
			'False,': 'false,',
			'False}': 'false}' ,
			'True,': 'true,',
			'True}': 'true}'}

	rep = dict((re.escape(k), v) for k, v in replaceItems.items())
	pattern = re.compile("|".join(rep.keys()))
	result = pattern.sub(lambda m: rep[re.escape(m.group(0))], doubleQuoted)
	#doubleQuoted = doubleQuoted.replace('None', 'null')
	#doubleQuoted = doubleQuoted.replace('False,', 'false,')
	#doubleQuoted = doubleQuoted.replace('True,', 'true,')
	return result

def sistemaTrans( transString ):

	logger.debug( '------------ INIT ----------sistemaTrans ---------------------')
	try : 
		
		if '__TRANSCODERMETADATA_MAMSEGMENTVIDEO__' in transString and len(transString) == len('__TRANSCODERMETADATA_MAMSEGMENTVIDEO__'):
			transString = '{}'

		
		#logger.debug(transString)
		#logger.debug(transString.replace('C"era',''))
		transString = transString.replace('C"era','')
		
		doubleQStr = singleQuoteToDoubleQuote( transString )
		#logger.debug(doubleQStr)
		data = json.loads( doubleQStr)
		#logger.debug(type(data))
		if 'binary' in data:
			del data['binary']
		result = json.dumps( data )
		#logger.debug(result)

	
	except Exception as e:
		logger.debug('Errore : ' + str(e))
		return [ False, 'errore nel json' ]
	return [ True, result ]
	




def flatten(d, parent_key='', sep='_'):
	items = []
	for k, v in d.items():
		new_key = parent_key + sep + k if parent_key else k
		try:
			items.extend(flatten(v, new_key, sep=sep).items())
		except:
			items.append((new_key, v))

	return dict(items)

def flatterRundown( jsonRundown ):
	# funzione che fa il parsing dell xml del rundown e ne restituisce un json con
	# i campi e i loro valori
	# quando poi si passera al json si presume che venga uguale
	result = []

	for jrun in jsonMpRundown:
		try:
			#logger.debug ( jsonMpRundown )
			result.append(flatten(jrun))
		except:
			logger.warning("problemi in flatterMpRundown")
			return []

	return result
	


if __name__ == "__main__":

	date = sistemaDateSitemap( 1695973254000 ) 
	logger.debug( date )
	logger.debug( ritornDateSitemapDecimal( date ) )


